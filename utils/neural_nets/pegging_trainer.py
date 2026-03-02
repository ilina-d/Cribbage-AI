import random

import torch
from torch import optim

from utils.neural_nets import BaseDiscardNet
from utils.helpers import DiscardEvaluator, CardDeck

from multiprocessing import Pool, cpu_count


class PeggingTrainer:
    """ Neural network trainer for the pegging phase. """

    pass


__all__ = ["PeggingTrainer"]