from utils.assets import Display
from utils.game import Game
from utils.simulator import Simulator
from utils.helpers import DiscardEvaluator, Scoring, StateEncoder

from utils.players import *
from utils.neural_nets import *

from utils.neural_nets.pegging_nets.PNT_DeepLeakySlim import PNT_DeepLeakySlim
from utils.neural_nets.pegging_nets.PNT_DeepReluSlim import PNT_DeepReluSlim
from utils.neural_nets.pegging_nets.PNT_DeepSeluSlim import PNT_DeepSeluSlim
from utils.neural_nets.pegging_nets.PNT_DeepSigmoidSlim import PNT_DeepSigmoidSlim
from utils.neural_nets.pegging_nets.PNT_DeepTanhSlim import PNT_DeepTanhSlim

from utils.neural_nets.pegging_nets.PNT_DeepLeakyWide import PNT_DeepLeakyWide
from utils.neural_nets.pegging_nets.PNT_DeepReluWide import PNT_DeepReluWide
from utils.neural_nets.pegging_nets.PNT_DeepSeluWide import PNT_DeepSeluWide
from utils.neural_nets.pegging_nets.PNT_DeepSigmoidWide import PNT_DeepSigmoidWide
from utils.neural_nets.pegging_nets.PNT_DeepTanhWide import PNT_DeepTanhWide

from utils.neural_nets.pegging_nets.PNT_ShallowLeakySlim import PNT_ShallowLeakySlim
from utils.neural_nets.pegging_nets.PNT_ShallowReluSlim import PNT_ShallowReluSlim
from utils.neural_nets.pegging_nets.PNT_ShallowSeluSlim import PNT_ShallowSeluSlim
from utils.neural_nets.pegging_nets.PNT_ShallowSigmoidSlim import PNT_ShallowSigmoidSlim
from utils.neural_nets.pegging_nets.PNT_ShallowTanhSlim import PNT_ShallowTanhSlim

from utils.neural_nets.pegging_nets.PNT_ShallowLeakyWide import PNT_ShallowLeakyWide
from utils.neural_nets.pegging_nets.PNT_ShallowReluWide import PNT_ShallowReluWide
from utils.neural_nets.pegging_nets.PNT_ShallowSeluWide import PNT_ShallowSeluWide
from utils.neural_nets.pegging_nets.PNT_ShallowSigmoidWide import PNT_ShallowSigmoidWide
from utils.neural_nets.pegging_nets.PNT_ShallowTanhWide import PNT_ShallowTanhWide


if __name__ == '__main__':

    TRAINING_ARGS = {
        'datasets': [
            '100K_states_recommended1'
        ],
        'lr' : 0.0001, 'wd' : 0.01, 'epochs' : 10_000, 'batch_size' : 10, 'pool_size' : 10,
        'alpha' : 1, 'alpha_step' : 10, 'alpha_decay' : 0.002, 'opponent' : DAPGPlayer()
    }

    NETS1 = [PNT_DeepReluSlim, PNT_DeepReluWide]
    NETS2 = [PNT_ShallowReluSlim, PNT_ShallowReluWide]
    NETS3 = [PNT_DeepSeluSlim, PNT_DeepSeluWide]
    NETS4 = [PNT_ShallowSeluSlim, PNT_ShallowSeluWide]
    NETS5 = [PNT_ShallowSigmoidSlim, PNT_ShallowSigmoidWide]

    # CONFIG #######################
    do_inf_adv = False
    RUNNING_NETS = NETS1
    ################################

    adv_type = 'InfAdv' if do_inf_adv else 'NormAdv'
    encoder = 'OriginalEncoder' if StateEncoder.LENGTH_CARD_INPUT == 17 else 'SimpleEncoder'

    for net in RUNNING_NETS:
        file_name = f'DzverTest_{encoder}_{net.__name__}_{adv_type}'
        net = net()
        PeggingTrainerPreLoaded.train(pegging_network = net, inflate_advantage = do_inf_adv, **TRAINING_ARGS)
        PeggingTrainerPreLoaded.save(net, file_name, '/')

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
