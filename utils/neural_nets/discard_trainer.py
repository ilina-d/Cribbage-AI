import random

import torch
from torch import optim

from utils.neural_nets import BaseDiscardNet
from utils.helpers import DiscardEvaluator, CardDeck


class DiscardTrainer:
    """ Neural network trainer for the discarding phase. """

    @classmethod
    def train(cls, discard_network: BaseDiscardNet, play_style: str, lr: float,
              wd: float, epochs: int, early_stop: bool = True) -> None:
        """
        Train the given discard neural network in the specified play style.

        ------

        Available play styles:
            - recommended: Reward based on statistical highest average score
            - sure_bet: Reward based on statistical highest minimum score
            - risky_bet: Reward based on statistical highest maximum score
            - hail_mary: Reward based on statistical best chance at a high score
            - aggressive: Reward based on statistical highest hand score
            - unsupervised: Reward based solely on points scored and confidence

        ------

        Arguments:
            discard_network: The discard network to be trained.
            play_style: The play style the net should be trained in.
            lr: The learning rate.
            wd: The weight decay.
            epochs: The number of epochs.
            early_stop: Whether to stop training early if results are satisfactory.

        ------

        Returns:
            The trained discard network.
        """

        net = discard_network.net
        optimizer = optim.AdamW(net.parameters(), lr = lr, weight_decay = wd)

        scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max = epochs, eta_min = 1e-5)

        net.train()

        for epoch in range(epochs):
            total_loss = 0

            for batch in range(64):
                deck = CardDeck(shuffle = True)
                player_hand = deck.deal_cards(6)
                opponent_hand = deck.deal_cards(6)
                starter_card = deck.deal_cards(1)[0]
                is_dealer = random.choice([True, False])
                player_score = random.randint(0, 120)
                opponent_score = random.randint(0, 120)

                card1, card2, conf1, conf2 = discard_network.get_discard_action(player_score, opponent_score,
                                                                            is_dealer, player_hand)

                if play_style == 'unsupervised':
                    player_hand_score = DiscardEvaluator.score_hand(player_hand, starter_card)
                    opponent_hand_score = DiscardEvaluator.score_hand(opponent_hand, starter_card)
                    crib_score = DiscardEvaluator.score_crib(player_hand + opponent_hand, starter_card)

                    reward = player_hand_score - opponent_hand_score
                    reward = reward + crib_score if is_dealer else reward - crib_score
                else:
                    ranked_pairs = DiscardEvaluator.get_discard_stats(player_hand, is_dealer)[play_style]
                    idx_loc = [card1 in cards and card2 in cards for cards, _ in ranked_pairs]
                    idx = idx_loc.index(True)

                    reward = 1 - idx / 14

                loss = -(conf1 + conf2) * reward
                total_loss += loss

            total_loss = total_loss / 64

            optimizer.zero_grad()
            total_loss.backward()
            optimizer.step()
            scheduler.step()

            print(f'Epoch: {epoch + 1}, Loss: {total_loss}')


    @classmethod
    def save(cls, discard_network: BaseDiscardNet, file_name: str, comment: str) -> None:
        """
        Save the trained discard network at /trained_nets/discard_nets/file_name.pt.

        ------

        Arguments:
            discard_network: The trained discard network.
            file_name: The file name
            comment: A comment to be saved along with the weights file.
        """

        torch.save(discard_network.net.state_dict(), f'trained_nets/discard_nets/{file_name}.pt')

        with open(f'trained_nets/discard_nets/{file_name}_comment.txt', 'w') as file:
            file.write(comment)


__all__ = ['DiscardTrainer']