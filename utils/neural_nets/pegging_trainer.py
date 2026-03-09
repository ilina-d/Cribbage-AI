import random

import torch
from torch import optim

from utils.neural_nets import BasePeggingNet
from utils.helpers import DiscardEvaluator, CardDeck, Scoring

from multiprocessing import Pool, cpu_count

from utils.players import BasePlayer


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

    deck = CardDeck(shuffle = True)
    player_hand, opponent_hand, starter_card = deck.deal_cards(6), deck.deal_cards(4), deck.deal_cards(1)[0]
    is_dealer = random.choice([True, False])
    score1, score2 = random.randint(0, 120), random.randint(0, 120)

    if play_style == 'random':
        player_hand.remove(random.choice(player_hand))
        player_hand.remove(random.choice(player_hand))
    else:
        ranked_pairs = DiscardEvaluator.get_discard_stats(player_hand, is_dealer)[play_style]
        best_cards = ranked_pairs[0][0]
        player_hand.remove(best_cards[0])
        player_hand.remove(best_cards[1])

    return {
        'cribs': [[], [], []],
        'current_crib_idx': 0,
        'crib_sums': [0, 0, 0],
        'starter_card': starter_card,
        'score1': score1,
        'score2': score2,
        'is_dealer': is_dealer,
        'player_hand': player_hand,
        'opponent_hand': opponent_hand
    }


def _run_episode(state: dict[str, ...], pegging_net: BasePeggingNet,
                 opponent: BasePlayer) -> tuple[list[torch.Tensor], list[int]]:
    """
    Run a sequence of actions that complete a pegging stage.

    ------

    Arguments:
        state: The initial game state going into a pegging phase.
        pegging_net: The pegging network being trained.
        opponent: The opponent player.

    ------

    Returns:
        The taken actions as two lists of their log-probabilities and immediate rewards.
    """

    called_go = False

    score1 = state['score1']
    score2 = state['score2']
    is_dealer = state['is_dealer']
    player_hand = state['player_hand'].copy()
    opponent_hand = state['opponent_hand'].copy()
    starter_card = state['starter_card']
    cribs = state['cribs']
    current_crib_idx = state['current_crib_idx']
    crib_sums = state['crib_sums'].copy()
    player1 = 'Me'
    player2 = opponent
    player2.cards = opponent_hand

    current_player = 'Me' if not is_dealer else opponent
    action_confs, action_scores = [], []

    while player_hand or opponent_hand:
        prev_called_go = called_go
        confidence = None

        if current_player == 'Me':
            current_crib_sum = crib_sums[current_crib_idx]
            current_crib_cards = cribs[current_crib_idx]
            distribution = pegging_net.get_distribution_policy(
                score1, score2, is_dealer, current_crib_sum, current_crib_cards, starter_card, player_hand
            )

            log_probs = torch.stack([card[1] for card in distribution])
            probs = torch.exp(log_probs)

            if probs.sum().item() <= 0 or torch.isnan(probs).any():
                played_card, confidence = distribution[log_probs.argmax().item()]
            else:
                played_card, confidence = distribution[torch.multinomial(probs, 1).item()]

            if played_card != 'GO':
                player_hand.remove(played_card)
        else:
            played_card = opponent.play_card({
                'cribs':  cribs, 'current_crib_idx': current_crib_idx, 'crib_sums': crib_sums,
                'starter_card': starter_card, 'dealer': player1 if is_dealer else player2,
                'player1': player1, 'player2': player2
            })

        if played_card == 'GO':
            if called_go:
                current_crib_idx += 1
                called_go = False
            else:
                called_go = True
                if current_player == opponent:
                    score1 += 1
                else:
                    score2 += 1

            if current_player == 'Me':
                action_confs.append(confidence)
                action_scores.append(0)
        else:
            cribs[current_crib_idx].append(played_card)
            score, _ = Scoring.score_card(state, current_player, update_points = False)
            crib_sums[current_crib_idx] += CardDeck.get_card_worth(played_card)

            if current_player == 'Me':
                action_confs.append(confidence)
                action_scores.append(score)
                score1 += score
            else:
                score2 += score

            if cribs[current_crib_idx] == 31:
                current_crib_idx += 1
                called_go = False

        if score1 >= 121 or score2 >= 121:
            break

        if not (called_go and called_go == prev_called_go):
            current_player = 'Me' if current_player == opponent else opponent

    return action_confs, action_scores



class PeggingTrainer:
    """ Neural network trainer for the pegging phase. """

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
    def train(cls, pegging_network: BasePeggingNet, lr: float, wd: float, epochs: int, opponent: BasePlayer,
              batch_size: int = 32, pool_size: int = 8, early_stop: bool = True, num_workers: int = 1) -> None:
        """
        Train the given pegging neural network using reinforced unsupervised learning.

        ------

        Arguments:
            pegging_network: The pegging network to be trained.
            lr: The learning rate.
            wd: The weight decay.
            epochs: The number of epochs.
            opponent: The opponent player.
            batch_size: The number of batches per epoch.
            pool_size: The number of sample states to generate per batch.
            early_stop: Whether to stop training early if results are satisfactory.
            num_workers: How many cores to use for training.
 
        ------

        Returns:
            The trained pegging network.
        """
        cls._training_logs = ''
        cls._log(
            f'{pegging_network.__class__.__name__} Structure Details:\n'
            f'{pegging_network.net}\n\n'
        )

        epoch_spaces = len(str(epochs))

        net = pegging_network.net
        optimizer = optim.AdamW(net.parameters(), lr = lr, weight_decay = wd)
        scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max = epochs, eta_min = 1e-5)

        num_workers = min(cpu_count(), num_workers)

        if pool_size % 20 != 0:
            cls._log(f'Pool size {pool_size} must be a divisible by 20.')
            pool_size = round(pool_size / 20) * 20
            cls._log(f'Pool size changed to {pool_size}.')

        if pool_size % num_workers != 0:
            cls._log(f'Pool size {pool_size} cannot be evenly distributed to {num_workers} workers.')

            if num_workers > pool_size:
                num_workers = pool_size
            else:
                num_workers = max([i for i in (1, 2, 3, 4, 5, 10, 20) if i < num_workers])

            cls._log(f'Number of workers changed to {num_workers}.')

        cls._log(
            f'{pegging_network.__class__.__name__} Training Details:\n'
            f'* Opponent: {opponent.__class__.__name__}\n'
            f'* Learning Rate: {lr}\n'
            f'* Weight Decay: {wd}\n'
            f'* Epochs: {epochs}\n'
            f'* Batch Size: {batch_size}\n'
            f'* Pool Size: {pool_size}\n'
            f'* Num Workers: {num_workers}\n'
            f'\n'
            f'* Early Stopping: {early_stop}\n'
        )

        cls._log(f'Training with {pegging_network.device}...')
        net.train()

        play_styles = ('recommended', 'aggressive', 'sure_bet', 'risky_bet', 'hail_mary')

        with Pool(processes = num_workers) as pool:
            for epoch in range(1, epochs + 1):
                total_loss, total_reward, total_points = 0, 0, 0
                optimizer.zero_grad()

                num_eval_discards = int(0.15 * pool_size)
                num_rand_discards = int(0.25 * pool_size)

                batch_data_args = [{'play_style': ps} for ps in play_styles] * num_eval_discards
                batch_data_args += [{'play_style': 'random'}] * num_rand_discards
                state_pool =  pool.map(_get_batch_data, batch_data_args)

                for _ in range(batch_size):
                    state = random.choice(state_pool)

                    action_confs, action_pts = _run_episode(state, pegging_network, opponent)

                    rewards = []
                    actual_reward = 0
                    for points in reversed(action_pts):
                        actual_reward += points
                        rewards.insert(0, actual_reward)

                    loss = torch.tensor(0.0, requires_grad=True)
                    for confidence, reward in zip(action_confs, rewards):
                        loss = loss + (-confidence * reward)

                    loss.backward()

                    total_loss += loss.item()
                    total_reward += sum(rewards)
                    total_points += rewards[0] if rewards else 0

                optimizer.step()
                scheduler.step()

                avg_loss = total_loss / batch_size
                avg_reward = total_reward / batch_size
                avg_points = total_points / batch_size

                cls._log(f'* Epoch: {epoch:<{epoch_spaces}}  |'
                         f'  Avg L: {avg_loss:<6.8f}'
                         f'  Avg R: {avg_reward:<4.8f}'
                         f'  Avg P: {avg_points:<4.8f}')

        cls._log('Training finished.')



    @classmethod
    def save(cls, pegging_network: BasePeggingNet, file_name: str, comment: str, logs: bool = True) -> None:
        """
        Save the trained pegging network at /trained_nets/pegging_nets/file_name.pt.

        ------

        Arguments:
            pegging_network: The trained pegging network.
            file_name: The file name
            comment: A comment to be saved along with the weights file.
            logs: Whether to include the training logs.
        """

        torch.save(pegging_network.net.state_dict(), f'trained_nets/pegging_nets/{file_name}.pt')

        if logs:
            comment += f'\n\n{cls._training_logs}'

        with open(f'trained_nets/pegging_nets/{file_name}_comment.txt', 'w') as file:
            file.write(comment)


__all__ = ["PeggingTrainer"]