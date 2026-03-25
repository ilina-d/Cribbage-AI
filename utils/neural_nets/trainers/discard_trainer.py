import random

import torch
from torch import optim

from utils.neural_nets import BaseDiscardNet
from utils.helpers import DiscardEvaluator, CardDeck

from multiprocessing import Pool, cpu_count


def _get_batch_data(args: dict[str, ...]) -> dict[str, ...]:
    """
    Generate input data for a single training batch.

    ------

    Arguments:
        args: A dictionary containing training info.

    ------

    Returns:
        A dictionary with the generated training data.
    """

    play_style = args['play_style']

    deck = CardDeck(shuffle=True)
    hand_cards, crib_cards, starter_card = deck.deal_cards(6), deck.deal_cards(2), deck.deal_cards(1)[0]
    is_dealer = random.choice([True, False])
    score1, score2 = random.randint(0, 120), random.randint(0, 120)

    ranked_pairs = DiscardEvaluator.get_discard_stats(hand_cards, is_dealer)[play_style]
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
        'baseline' : baseline
    }


class DiscardTrainer:
    """ Neural network trainer for the discarding phase. """

    BEST_HAND_SCORE = 29  # four 5s and a Jack with the same suit as the starter card
    BEST_CRIB_SCORE = 29  # same as hand
    BEST_OUTCOME = 53     # best hand + 6644 in crib
    WORST_OUTCOME = 0 - BEST_CRIB_SCORE  # nothing scored in hand
    _training_logs: str = ''


    @classmethod
    def _log(cls, text: str) -> None:
        """
        Print and expand the training logs.

        ------

        Arguments:
             text: The log text.
        """

        cls._training_logs += f'{text}\n'
        print(text)


    @classmethod
    def train(cls, discard_network: BaseDiscardNet, lr: float, wd: float, epochs: int, batch_size: int = 32,
              pool_size: int = 8, play_style: str = 'recommended', num_workers: int = 1,
              alpha: float = 0.0, alpha_decay: float = 0.95, alpha_step: int = 10,
              accumulate_loss: bool = False, inflate_advantage: bool = False) -> None:
        """
        Train the given discard neural network using reinforced supervised or unsupervised learning.

        Unsupervised is used when alpha = 0. While supervised is used when play_style != None and alpha > 0.

        ------

        Available play styles:
            - recommended: Reward based on statistical highest average score.
            - sure_bet: Reward based on statistical highest minimum score.
            - risky_bet: Reward based on statistical highest maximum score.
            - hail_mary: Reward based on statistical best chance at a high score.
            - aggressive: Reward based on statistical highest hand score.

        ------

        Arguments:
            discard_network: The discard network to be trained.
            lr: The learning rate.
            wd: The weight decay.
            epochs: The number of epochs.
            batch_size: The number of batches per epoch.
            pool_size: The number of sample states to generate per batch.
            play_style: The play style the net should be trained in.
                        The same play style is used to calculate a reward baseline even when unsupervised.
                        Defaults to "recommended".
            alpha: How reliant the network is on the given play-style initially.
            alpha_decay: By how much to reduce the network's dependency of the given play-style.
            alpha_step: How often to decay alpha in epochs.
            num_workers: How many cores to use for training.
            accumulate_loss: Whether to accumulate gradient loss within a batch before stepping.
            inflate_advantage: Whether to inflate the calculated advantage.

        ------

        Returns:
            The trained discard network.
        """

        cls._training_logs = ''
        cls._log(
            f'{discard_network.__class__.__name__} Structure Details:\n'
            f'{discard_network.net}\n\n'
        )

        epoch_spaces = len(str(epochs))

        net = discard_network.net
        optimizer = optim.AdamW(net.parameters(), lr = lr, weight_decay = wd)
        scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max = epochs, eta_min = lr / 100)

        num_workers = min(cpu_count(), num_workers)

        cls._log(
            f'{discard_network.__class__.__name__} Training Details:\n'
            f'* Learning Rate: {lr}\n'
            f'* Weight Decay: {wd}\n'
            f'* Epochs: {epochs}\n'
            f'* Batch Size: {batch_size}\n'
            f'* Pool Size: {pool_size}\n'
            f'* Num Workers: {num_workers}\n'
            f'\n'
            f'* Accumulate loss: {accumulate_loss}\n'
            f'* Inflated advantage: {inflate_advantage}\n'
            f'\n'
            f'* Supervised: {alpha > 0}\n'
            f'* Alpha: {alpha}\n'
            f'* Alpha Decay: {alpha_decay}\n'
            f'* Alpha Step: {alpha_step}\n\n'
        )

        cls._log(f'Training with {discard_network.device}...')
        net.train()

        with Pool(processes = num_workers) as pool:
            batch_data_args = [{'play_style': play_style} for _ in range(pool_size * epochs)]
            state_pool_generator = pool.imap(_get_batch_data, batch_data_args, chunksize = pool_size)

            for epoch in range(1, epochs + 1):
                total_loss, total_reward, total_advantage = 0, 0, 0
                if accumulate_loss:
                    optimizer.zero_grad()

                state_pool = [next(state_pool_generator) for _ in range(pool_size)]

                for _ in range(batch_size):
                    state = random.choice(state_pool)
                    hand_cards = state['hand_cards'].copy()
                    crib_cards = state['crib_cards'].copy()
                    is_dealer = state['is_dealer']
                    starter_card = state['starter_card']

                    rely_on_coach = random.choices([True, False], [alpha, 1 - alpha], k = 1)[0]
                    distribution = discard_network.get_distribution_policy(
                        state['score1'], state['score2'], is_dealer, hand_cards
                    )

                    if rely_on_coach:
                        best_pair = state['best_cards']
                        card1, card2 = best_pair[0], best_pair[1]
                        confidence = discard_network.get_combo_confidence(
                            distribution, card1, card2
                        )

                    else:
                        log_probs = torch.stack([combo[2] for combo in distribution])
                        probs = torch.exp(log_probs)

                        chosen_combo = distribution[torch.multinomial(probs, 1).item()]
                        card1, card2, confidence = chosen_combo[0], chosen_combo[1], chosen_combo[2]

                    hand_cards.remove(card1)
                    hand_cards.remove(card2)
                    crib_cards.extend([card1, card2])
                    hand_score = DiscardEvaluator.score_hand(hand_cards, starter_card)
                    crib_score = DiscardEvaluator.score_crib(crib_cards, starter_card)

                    # reward range is [-29, 53]
                    reward = hand_score + crib_score if is_dealer else hand_score - crib_score
                    baseline = state['baseline']
                    advantage = reward - baseline

                    if inflate_advantage:
                        advantage = advantage ** 3

                    if not accumulate_loss:
                        optimizer.zero_grad()

                    loss = -confidence * advantage

                    loss.backward()

                    # if inflate_advantage:
                    #     torch.nn.utils.clip_grad_norm_(net.parameters(), max_norm = 5.0)

                    if not accumulate_loss:
                        optimizer.step()

                    total_loss += loss.item()
                    total_reward += reward
                    total_advantage += advantage

                if accumulate_loss:
                    # if inflate_advantage:
                    #     torch.nn.utils.clip_grad_norm_(net.parameters(), max_norm = 5.0)
                    optimizer.step()

                scheduler.step()

                avg_loss = total_loss / batch_size
                avg_reward = total_reward / batch_size
                avg_advantage = total_advantage / batch_size

                if alpha_step > 0 and epoch % alpha_step == 0 and alpha > 0:
                    alpha = max(alpha - alpha_decay, 0)

                cls._log(
                    f'* Epoch: {epoch:<{epoch_spaces}} '
                    f'| Avg L: {avg_loss:<15.8f} '
                    f'| Avg R: {avg_reward:<15.8f} '
                    f'| Avg A: {avg_advantage:<15.8f} '
                    f'| Alpha: {alpha:<15.8f}'
                )

        cls._log('Training finished.')


    @classmethod
    def save(cls, discard_network: BaseDiscardNet, file_name: str, comment: str, logs: bool = True) -> None:
        """
        Save the trained discard network at /trained_nets/discard_nets/file_name.pt.

        ------

        Arguments:
            discard_network: The trained discard network.
            file_name: The file name
            comment: A comment to be saved along with the weights file.
            logs: Whether to include the training logs.
        """

        torch.save(discard_network.net.state_dict(), f'trained_nets/discard_nets/{file_name}.pt')

        if logs:
            comment += f'\n\n{cls._training_logs}'

        with open(f'trained_nets/discard_nets/{file_name}_comment.txt', 'w') as file:
            file.write(comment)


__all__ = ['DiscardTrainer']
