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


if __name__ == '__main__':

    TRAINING_ARGS = {
        'datasets': [
            '100K_states_recommended1', '100K_states_recommended2', '100K_states_recommended3',
            '100K_states_recommended4', '100K_states_recommended5'
        ],
        'lr' : 0.0001, 'wd' : 0.01, 'epochs' : 50_000, 'batch_size' : 10, 'pool_size' : 10,
        'alpha' : 1, 'alpha_step' : 50, 'alpha_decay' : 0.002
    }

    # net = DNT_ShallowTanhWide()
    # DiscardTrainerPreLoaded.train(discard_network = net, inflate_advantage = False, **TRAINING_ARGS)
    # DiscardTrainerPreLoaded.save(
    #     discard_network = net,
    #     file_name = 'PepaSigmoidTest_TanhShallowWide_NormAdv_SimpleEncoder',
    #     comment = '/'
    # )

    # net = DNT_ShallowTanhWide()
    # DiscardTrainerPreLoaded.train(discard_network = net, inflate_advantage = True, **TRAINING_ARGS)
    # DiscardTrainerPreLoaded.save(
    #     discard_network = net,
    #     file_name = 'PepaSigmoidTest_TanhShallowWide_InfAdv_SimpleEncoder',
    #     comment = '/'
    # )

    # TODO: Highlighting for Tanh with Original Encoder

    # net = DNT_ShallowTanhWide()
    # DiscardTrainerPreLoaded.train(discard_network = net, inflate_advantage = False, **TRAINING_ARGS)
    # DiscardTrainerPreLoaded.save(
    #     discard_network = net,
    #     file_name = 'PepaSigmoidTest_TanhShallowWide_NormAdv_OriginalEncoder',
    #     comment = '/'
    # )

    # net = DNT_ShallowTanhWide()
    # DiscardTrainerPreLoaded.train(discard_network = net, inflate_advantage = True, **TRAINING_ARGS)
    # DiscardTrainerPreLoaded.save(
    #     discard_network = net,
    #     file_name = 'PepaSigmoidTest_TanhShallowWide_InfAdv_OriginalEncoder',
    #     comment = '/'
    # )

    # TODO: Highlight end

    # net = DNT_ShallowSeluSlim()
    # DiscardTrainerPreLoaded.train(discard_network = net, inflate_advantage = False, **TRAINING_ARGS)
    # DiscardTrainerPreLoaded.save(
    #     discard_network = net,
    #     file_name = 'PepaSigmoidTest_SeluShallowSlim_NormAdv_SimpleEncoder',
    #     comment = '/'
    # )

    # net = DNT_ShallowSeluSlim()
    # DiscardTrainerPreLoaded.train(discard_network = net, inflate_advantage = True, **TRAINING_ARGS)
    # DiscardTrainerPreLoaded.save(
    #     discard_network = net,
    #     file_name = 'PepaSigmoidTest_SeluShallowSlim_InfAdv_SimpleEncoder',
    #     comment = '/'
    # )

    # net = DNT_ShallowSeluWide()
    # DiscardTrainerPreLoaded.train(discard_network = net, inflate_advantage = False, **TRAINING_ARGS)
    # DiscardTrainerPreLoaded.save(
    #     discard_network = net,
    #     file_name = 'PepaSigmoidTest_SeluShallowWide_NormAdv_SimpleEncoder',
    #     comment = '/'
    # )

    # net = DNT_ShallowSeluWide()
    # DiscardTrainerPreLoaded.train(discard_network = net, inflate_advantage = True, **TRAINING_ARGS)
    # DiscardTrainerPreLoaded.save(
    #     discard_network = net,
    #     file_name = 'PepaSigmoidTest_SeluShallowWide_InfAdv_SimpleEncoder',
    #     comment = '/'
    # )

    # net = DNT_DeepSeluSlim()
    # DiscardTrainerPreLoaded.train(discard_network = net, inflate_advantage = False, **TRAINING_ARGS)
    # DiscardTrainerPreLoaded.save(
    #     discard_network = net,
    #     file_name = 'PepaSigmoidTest_SeluDeepSlim_NormAdv_SimpleEncoder',
    #     comment = '/'
    # )

    # net = DNT_DeepSeluSlim()
    # DiscardTrainerPreLoaded.train(discard_network = net, inflate_advantage = True, **TRAINING_ARGS)
    # DiscardTrainerPreLoaded.save(
    #     discard_network = net,
    #     file_name = 'PepaSigmoidTest_SeluDeepSlim_InfAdv_SimpleEncoder',
    #     comment = '/'
    # )

    # net = DNT_DeepSeluWide()
    # DiscardTrainerPreLoaded.train(discard_network = net, inflate_advantage = False, **TRAINING_ARGS)
    # DiscardTrainerPreLoaded.save(
    #     discard_network = net,
    #     file_name = 'PepaSigmoidTest_SeluDeepWide_NormAdv_SimpleEncoder',
    #     comment = '/'
    # )

    # net = DNT_DeepSeluWide()
    # DiscardTrainerPreLoaded.train(discard_network = net, inflate_advantage = True, **TRAINING_ARGS)
    # DiscardTrainerPreLoaded.save(
    #     discard_network = net,
    #     file_name = 'PepaSigmoidTest_SeluDeepWide_InfAdv_SimpleEncoder',
    #     comment = '/'
    # )

    # TODO: Highliting for Selu with Original Encoder

    # net = DNT_ShallowSeluSlim()
    # DiscardTrainerPreLoaded.train(discard_network = net, inflate_advantage = False, **TRAINING_ARGS)
    # DiscardTrainerPreLoaded.save(
    #     discard_network = net,
    #     file_name = 'PepaSigmoidTest_SeluShallowSlim_NormAdv_OriginalEncoder',
    #     comment = '/'
    # )
    #
    # net = DNT_ShallowSeluSlim()
    # DiscardTrainerPreLoaded.train(discard_network = net, inflate_advantage = True, **TRAINING_ARGS)
    # DiscardTrainerPreLoaded.save(
    #     discard_network = net,
    #     file_name = 'PepaSigmoidTest_SeluShallowSlim_InfAdv_OriginalEncoder',
    #     comment = '/'
    # )
    #
    # net = DNT_ShallowSeluWide()
    # DiscardTrainerPreLoaded.train(discard_network = net, inflate_advantage = False, **TRAINING_ARGS)
    # DiscardTrainerPreLoaded.save(
    #     discard_network = net,
    #     file_name = 'PepaSigmoidTest_SeluShallowWide_NormAdv_OriginalEncoder',
    #     comment = '/'
    # )
    #
    # net = DNT_ShallowSeluWide()
    # DiscardTrainerPreLoaded.train(discard_network = net, inflate_advantage = True, **TRAINING_ARGS)
    # DiscardTrainerPreLoaded.save(
    #     discard_network = net,
    #     file_name = 'PepaSigmoidTest_SeluShallowWide_InfAdv_OriginalEncoder',
    #     comment = '/'
    # )
    #
    # net = DNT_DeepSeluSlim()
    # DiscardTrainerPreLoaded.train(discard_network = net, inflate_advantage = False, **TRAINING_ARGS)
    # DiscardTrainerPreLoaded.save(
    #     discard_network = net,
    #     file_name = 'PepaSigmoidTest_SeluDeepSlim_NormAdv_OriginalEncoder',
    #     comment = '/'
    # )
    #
    # net = DNT_DeepSeluSlim()
    # DiscardTrainerPreLoaded.train(discard_network = net, inflate_advantage = True, **TRAINING_ARGS)
    # DiscardTrainerPreLoaded.save(
    #     discard_network = net,
    #     file_name = 'PepaSigmoidTest_SeluDeepSlim_InfAdv_OriginalEncoder',
    #     comment = '/'
    # )
    #
    # net = DNT_DeepSeluWide()
    # DiscardTrainerPreLoaded.train(discard_network = net, inflate_advantage = False, **TRAINING_ARGS)
    # DiscardTrainerPreLoaded.save(
    #     discard_network = net,
    #     file_name = 'PepaSigmoidTest_SeluDeepWide_NormAdv_OriginalEncoder',
    #     comment = '/'
    # )
    #
    # net = DNT_DeepSeluWide()
    # DiscardTrainerPreLoaded.train(discard_network = net, inflate_advantage = True, **TRAINING_ARGS)
    # DiscardTrainerPreLoaded.save(
    #     discard_network = net,
    #     file_name = 'PepaSigmoidTest_SeluDeepWide_InfAdv_OriginalEncoder',
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
