from utils.assets import Display
from utils.game import Game
from utils.simulator import Simulator
from utils.helpers import DiscardEvaluator, Scoring

from utils.players import *
from utils.neural_nets import *

from utils.neural_nets.discard_nets.DNT_DeepLeakySlim import DNT_DeepLeakySlim
from utils.neural_nets.discard_nets.DNT_DeepReluSlim import DNT_DeepReluSlim
from utils.neural_nets.discard_nets.DNT_DeepSeluSlim import DNT_DeepSeluSlim
from utils.neural_nets.discard_nets.DNT_DeepSigmoidSlim import DNT_DeepSigmoidSlim
from utils.neural_nets.discard_nets.DNT_DeepTanhSlim import DNT_DeepTanhSlim

from utils.neural_nets.discard_nets.DNT_DeepLeakyWide import DNT_DeepLeakyWide
from utils.neural_nets.discard_nets.DNT_DeepReluWide import DNT_DeepReluWide
from utils.neural_nets.discard_nets.DNT_DeepSeluWide import DNT_DeepSeluWide
from utils.neural_nets.discard_nets.DNT_DeepSigmoidWide import DNT_DeepSigmoidWide
from utils.neural_nets.discard_nets.DNT_DeepTanhWide import DNT_DeepTanhWide

from utils.neural_nets.discard_nets.DNT_ShallowLeakySlim import DNT_ShallowLeakySlim
from utils.neural_nets.discard_nets.DNT_ShallowReluSlim import DNT_ShallowReluSlim
from utils.neural_nets.discard_nets.DNT_ShallowSeluSlim import DNT_ShallowSeluSlim
from utils.neural_nets.discard_nets.DNT_ShallowSigmoidSlim import DNT_ShallowSigmoidSlim
from utils.neural_nets.discard_nets.DNT_ShallowTanhSlim import DNT_ShallowTanhSlim

from utils.neural_nets.discard_nets.DNT_ShallowLeakyWide import DNT_ShallowLeakyWide
from utils.neural_nets.discard_nets.DNT_ShallowReluWide import DNT_ShallowReluWide
from utils.neural_nets.discard_nets.DNT_ShallowSeluWide import DNT_ShallowSeluWide
from utils.neural_nets.discard_nets.DNT_ShallowSigmoidWide import DNT_ShallowSigmoidWide
from utils.neural_nets.discard_nets.DNT_ShallowTanhWide import DNT_ShallowTanhWide


from multiprocessing import Pool
import random
from utils.helpers import CardDeck
import time
import json


def _generate_state(args: dict[str, ...]) -> dict[str, ...]:
    """
    Generate input data for a single training batch.

    ------

    Arguments:
        args: A dictionary containing training info.

    ------

    Returns:
        A dictionary with the generated training data.
    """

    deck = CardDeck(shuffle=True)
    hand_cards, crib_cards, starter_card = deck.deal_cards(6), deck.deal_cards(2), deck.deal_cards(1)[0]
    is_dealer = random.choice([True, False])
    score1, score2 = random.randint(0, 120), random.randint(0, 120)

    ranked_pairs = DiscardEvaluator.get_discard_stats(hand_cards, is_dealer)['recommended']
    best_cards = ranked_pairs[0][0]

    baseline = sum([score for _, score in ranked_pairs]) / 15

    return {
        'score1': score1,
        'score2': score2,
        'is_dealer': is_dealer,
        'hand_cards': hand_cards,
        'crib_cards': crib_cards,
        'starter_card': starter_card,
        'best_cards': best_cards,
        'baseline' : baseline,
        'ranked_pairs' : ranked_pairs
    }


if __name__ == '__main__':

    num_workers = 20
    with Pool(processes = num_workers) as pool:

        print('[ GENERATOR ] : Preparing...', end = '\r')

        for iteration in range(1, 10 + 1):
            num_states = 100_000
            all_states = []

            time_start = time.time()
            for n, state in enumerate(pool.imap_unordered(_generate_state, [{}] * num_states), start = 1):
                all_states.append(state)

                percent_done = (n / num_states) * 100
                time_passed = time.time() - time_start
                hours = int(time_passed // 3600)
                minutes = int((time_passed % 3600) // 60)
                seconds = int(time_passed % 60)
                time_string = f'{hours}h {minutes}m {seconds}s'

                print(
                    f'\r\033[K'
                    f'[ GENERATOR ] Generating states...   '
                    f'Iteration #{iteration} | '
                    f'{str(round(percent_done, 2)) + "%":<6} '
                    f'<{"=" * int(percent_done)}{"-" * int(100 - int(percent_done))}> '
                    f'| Time Passed: {time_string}', end = ''
                )

            with open(f'datasets/discard_datasets/100K_states_recommended{iteration}.json', 'w') as file:
                json.dump(all_states, file)

            print('\n')

    input('... all done ...')


    TRAINING_ARGS = {
        'lr' : 0.0001, 'wd' : 0.01, 'epochs' : 50_000, 'batch_size' : 10, 'pool_size' : 10,
        'num_workers' : 20, 'alpha' : 1, 'alpha_step' : 50, 'alpha_decay' : 0.002
    }

    net = DNT_ShallowTanhWide()
    DiscardTrainer.train(discard_network = net, inflate_advantage = False, **TRAINING_ARGS)
    DiscardTrainer.save(
        discard_network = net,
        file_name = 'PepaTest_TanhShallowWide_NormAdv_SimpleEncoder',
        comment = '/'
    )

    net = DNT_ShallowTanhWide()
    DiscardTrainer.train(discard_network = net, inflate_advantage = True, **TRAINING_ARGS)
    DiscardTrainer.save(
        discard_network = net,
        file_name = 'PepaTest_TanhShallowWide_InfAdv_SimpleEncoder',
        comment = '/'
    )

    # net = DNT_ShallowTanhWide()
    # DiscardTrainer.train(discard_network = net, inflate_advantage = False, **TRAINING_ARGS)
    # DiscardTrainer.save(
    #     discard_network = net,
    #     file_name = 'PepaTest_TanhShallowWide_NormAdv_OriginalEncoder',
    #     comment = '/'
    # )
    #
    # net = DNT_ShallowTanhWide()
    # DiscardTrainer.train(discard_network = net, inflate_advantage = True, **TRAINING_ARGS)
    # DiscardTrainer.save(
    #     discard_network = net,
    #     file_name = 'PepaTest_TanhShallowWide_InfAdv_OriginalEncoder',
    #     comment = '/'
    # )

    net = DNT_ShallowSeluSlim()
    DiscardTrainer.train(discard_network = net, inflate_advantage = False, **TRAINING_ARGS)
    DiscardTrainer.save(
        discard_network = net,
        file_name = 'PepaTest_SeluShallowSlim_NormAdv_SimpleEncoder',
        comment = '/'
    )

    net = DNT_ShallowSeluSlim()
    DiscardTrainer.train(discard_network = net, inflate_advantage = True, **TRAINING_ARGS)
    DiscardTrainer.save(
        discard_network = net,
        file_name = 'PepaTest_SeluShallowSlim_InfAdv_SimpleEncoder',
        comment = '/'
    )

    net = DNT_ShallowSeluWide()
    DiscardTrainer.train(discard_network = net, inflate_advantage = False, **TRAINING_ARGS)
    DiscardTrainer.save(
        discard_network = net,
        file_name = 'PepaTest_SeluShallowWide_NormAdv_SimpleEncoder',
        comment = '/'
    )

    net = DNT_ShallowSeluWide()
    DiscardTrainer.train(discard_network = net, inflate_advantage = True, **TRAINING_ARGS)
    DiscardTrainer.save(
        discard_network = net,
        file_name = 'PepaTest_SeluShallowWide_InfAdv_SimpleEncoder',
        comment = '/'
    )

    net = DNT_DeepSeluSlim()
    DiscardTrainer.train(discard_network = net, inflate_advantage = False, **TRAINING_ARGS)
    DiscardTrainer.save(
        discard_network = net,
        file_name = 'PepaTest_SeluDeepSlim_NormAdv_SimpleEncoder',
        comment = '/'
    )

    net = DNT_DeepSeluSlim()
    DiscardTrainer.train(discard_network = net, inflate_advantage = True, **TRAINING_ARGS)
    DiscardTrainer.save(
        discard_network = net,
        file_name = 'PepaTest_SeluDeepSlim_InfAdv_SimpleEncoder',
        comment = '/'
    )

    net = DNT_DeepSeluWide()
    DiscardTrainer.train(discard_network = net, inflate_advantage = False, **TRAINING_ARGS)
    DiscardTrainer.save(
        discard_network = net,
        file_name = 'PepaTest_SeluDeepWide_NormAdv_SimpleEncoder',
        comment = '/'
    )

    net = DNT_DeepSeluWide()
    DiscardTrainer.train(discard_network = net, inflate_advantage = True, **TRAINING_ARGS)
    DiscardTrainer.save(
        discard_network = net,
        file_name = 'PepaTest_SeluDeepWide_InfAdv_SimpleEncoder',
        comment = '/'
    )

    # net = DNT_ShallowSeluSlim()
    # DiscardTrainer.train(discard_network = net, inflate_advantage = False, **TRAINING_ARGS)
    # DiscardTrainer.save(
    #     discard_network = net,
    #     file_name = 'PepaTest_SeluShallowSlim_NormAdv_OriginalEncoder',
    #     comment = '/'
    # )
    #
    # net = DNT_ShallowSeluSlim()
    # DiscardTrainer.train(discard_network = net, inflate_advantage = True, **TRAINING_ARGS)
    # DiscardTrainer.save(
    #     discard_network = net,
    #     file_name = 'PepaTest_SeluShallowSlim_InfAdv_OriginalEncoder',
    #     comment = '/'
    # )
    #
    # net = DNT_ShallowSeluWide()
    # DiscardTrainer.train(discard_network = net, inflate_advantage = False, **TRAINING_ARGS)
    # DiscardTrainer.save(
    #     discard_network = net,
    #     file_name = 'PepaTest_SeluShallowWide_NormAdv_OriginalEncoder',
    #     comment = '/'
    # )
    #
    # net = DNT_ShallowSeluWide()
    # DiscardTrainer.train(discard_network = net, inflate_advantage = True, **TRAINING_ARGS)
    # DiscardTrainer.save(
    #     discard_network = net,
    #     file_name = 'PepaTest_SeluShallowWide_InfAdv_OriginalEncoder',
    #     comment = '/'
    # )
    #
    # net = DNT_DeepSeluSlim()
    # DiscardTrainer.train(discard_network = net, inflate_advantage = False, **TRAINING_ARGS)
    # DiscardTrainer.save(
    #     discard_network = net,
    #     file_name = 'PepaTest_SeluDeepSlim_NormAdv_OriginalEncoder',
    #     comment = '/'
    # )
    #
    # net = DNT_DeepSeluSlim()
    # DiscardTrainer.train(discard_network = net, inflate_advantage = True, **TRAINING_ARGS)
    # DiscardTrainer.save(
    #     discard_network = net,
    #     file_name = 'PepaTest_SeluDeepSlim_InfAdv_OriginalEncoder',
    #     comment = '/'
    # )
    #
    # net = DNT_DeepSeluWide()
    # DiscardTrainer.train(discard_network = net, inflate_advantage = False, **TRAINING_ARGS)
    # DiscardTrainer.save(
    #     discard_network = net,
    #     file_name = 'PepaTest_SeluDeepWide_NormAdv_OriginalEncoder',
    #     comment = '/'
    # )
    #
    # net = DNT_DeepSeluWide()
    # DiscardTrainer.train(discard_network = net, inflate_advantage = True, **TRAINING_ARGS)
    # DiscardTrainer.save(
    #     discard_network = net,
    #     file_name = 'PepaTest_SeluDeepWide_InfAdv_OriginalEncoder',
    #     comment = '/'
    # )

    input('... preventing program from continuing by waiting for input ...\n'
          '... full-screen the terminal before continuing ...')

    game = Game(
        player1 = UserPlayer(),
        player2 = DAPGPlayer(),
        first_dealer = None,
        wait_after_move = 200,
        wait_after_info = True,
        show_opponents_hand = False,
        visuals = True,
        measure_statistics = False
    )

    game.play()

    input('... preventing program from continuing by waiting for input ...')
