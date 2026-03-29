import json
import random

import torch
from torch import optim

from utils.neural_nets import BasePeggingNet
from utils.helpers import CardDeck, Scoring

from utils.players import BasePlayer
from utils.players.dapg_player import DAPGPlayer


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
    alpha = state['alpha']

    current_player = 'Me' if not is_dealer else opponent
    action_confs, action_scores = [], []

    coach = DAPGPlayer()

    while player_hand or opponent_hand:
        prev_called_go = called_go
        confidence = None

        reduced_state = {
            'cribs': cribs, 'current_crib_idx': current_crib_idx, 'crib_sums': crib_sums,
            'starter_card': starter_card, 'dealer': player1 if is_dealer else player2,
            'player1': player1, 'player2': player2
        }

        if current_player == 'Me':
            current_crib_sum = crib_sums[current_crib_idx]
            current_crib_cards = cribs[current_crib_idx]
            distribution = pegging_net.get_distribution_policy(
                score1, score2, current_crib_sum, current_crib_cards, player_hand
            )

            rely_on_coach = random.choices([True, False], [alpha, 1 - alpha], k=1)[0]
            if rely_on_coach:
                coach.cards = player_hand

                played_card = coach.play_card(reduced_state)
                confidence = pegging_net.get_card_confidence(distribution, played_card)
            else:
                log_probs = torch.stack([card[1] for card in distribution])
                probs = torch.exp(log_probs)

                played_card, confidence = distribution[torch.multinomial(probs, 1).item()]

            if played_card != 'GO' and not rely_on_coach:
                player_hand.remove(played_card)
        else:
            played_card = opponent.play_card(reduced_state)

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
            score, _ = Scoring.score_card(state, current_player, update_points=False)
            crib_sums[current_crib_idx] += CardDeck.get_card_worth(played_card)

            if current_player == 'Me':
                action_confs.append(confidence)
                action_scores.append(score)
                score1 += score
            else:
                score2 += score

            if crib_sums[current_crib_idx] == 31:
                current_crib_idx += 1
                called_go = False

        if score1 >= 121 or score2 >= 121:
            break

        if not (called_go and called_go == prev_called_go):
            current_player = 'Me' if current_player == opponent else opponent

    return action_confs, action_scores


class PeggingTrainerPreLoaded:
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
    def train(cls, pegging_network: BasePeggingNet, datasets: list[str], lr: float, wd: float,
              opponent: BasePlayer, epochs: int, batch_size: int = 32, pool_size: int = 8,
              alpha: float = 0.0, alpha_decay: float = 0.95, alpha_step: int = 10,
              accumulate_loss: bool = False, inflate_advantage: bool = False) -> None:
        """
        Train the given pegging neural network using reinforced supervised or unsupervised learning.

        Unsupervised is used when alpha = 0. While supervised is used when alpha > 0.

        ------

        Arguments:
            pegging_network: The pegging network to be trained.
            lr: The learning rate.
            wd: The weight decay.
            epochs: The number of epochs.
            opponent: The opponent player.
            batch_size: The number of batches per epoch.
            pool_size: The number of sample states to generate per batch.
            alpha: How reliant the network is on the coach (GreedyPlayer).
            alpha_decay: By how much to reduce the network's dependency on the coach.
            alpha_step: How often to decay alpha in epochs.
            accumulate_loss: Whether to accumulate gradient loss within a batch before stepping.
            inflate_advantage: Whether to inflate the calculated advantage.
            datasets: List of dataset names to use as state pools during training.

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
        optimizer = optim.AdamW(net.parameters(), lr=lr, weight_decay=wd)
        scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs, eta_min=1e-5)

        if pool_size % 5 != 0:
            cls._log(f'Pool size {pool_size} must be a divisible by 5.')
            pool_size = round(pool_size / 5) * 5
            cls._log(f'Pool size changed to {pool_size}.')

        cls._log(
            f'{pegging_network.__class__.__name__} Training Details:\n'
            f'* Datasets: {", ".join(datasets)}'
            f'* Opponent: {opponent.__class__.__name__}\n'
            f'* Learning Rate: {lr}\n'
            f'* Weight Decay: {wd}\n'
            f'* Epochs: {epochs}\n'
            f'* Batch Size: {batch_size}\n'
            f'* Pool Size: {pool_size}\n'
            f'\n'
            f'* Accumulate loss: {accumulate_loss}\n'
            f'* Inflated advantage: {inflate_advantage}\n'
            f'\n'
            f'* Supervised: {alpha > 0}\n'
            f'* Alpha: {alpha}\n'
            f'* Alpha Decay: {alpha_decay}\n'
            f'* Alpha Step: {alpha_step}\n\n'
        )

        total_state_pool = []
        for dataset in datasets:
            cls._log(f'Preloading states from "{dataset}.json"...')
            with open(f'datasets/pegging_datasets/{dataset}.json', 'r') as file:
                data = json.load(file)
                total_state_pool.extend(data)
        total_state_pool_len = len(total_state_pool)

        cls._log(f'Training with {pegging_network.device}...')
        net.train()

        state_pool_count = -1
        for epoch in range(1, epochs + 1):
            total_loss, total_reward, total_points = 0, 0, 0

            if accumulate_loss:
                optimizer.zero_grad()

            state_pool_count += 1
            idx1 = state_pool_count * pool_size
            idx2 = state_pool_count * pool_size + pool_size - 1

            if idx1 >= total_state_pool_len or idx2 >= total_state_pool_len:
                cls._log(f'| {"WARNING:":<{7 + epoch_spaces}} | State pool elapsed at epoch {epoch} '
                         f'due to slice index being out of range: total_state_pool[ {idx1} : {idx2} ].')
                state_pool_count = 0
                idx1 = state_pool_count * pool_size
                idx2 = state_pool_count * pool_size + pool_size - 1

            state_pool = total_state_pool[idx1: idx2]

            for _ in range(batch_size):
                state = random.choice(state_pool)
                state['alpha'] = alpha

                action_confs, action_pts = _run_episode(state, pegging_network, opponent)

                rewards = []
                actual_reward = 0
                for points in reversed(action_pts):
                    actual_reward += points
                    rewards.insert(0, actual_reward)

                loss = torch.tensor(0.0, requires_grad = True)
                for confidence, reward in zip(action_confs, rewards):
                    if inflate_advantage:
                        reward = reward ** 2
                    loss = loss + (-confidence * reward)

                if not accumulate_loss:
                    optimizer.zero_grad()

                loss.backward()

                # if inflate_advantage:
                #     torch.nn.utils.clip_grad_norm_(net.parameters(), max_norm = 5.0)

                if not accumulate_loss:
                    optimizer.step()

                total_loss += loss.item()
                total_reward += sum(rewards)
                total_points += rewards[0] if rewards else 0

            if accumulate_loss:
                # if inflate_advantage:
                #     torch.nn.utils.clip_grad_norm_(net.parameters(), max_norm = 5.0)
                optimizer.step()
            scheduler.step()

            avg_loss = total_loss / batch_size
            avg_reward = total_reward / batch_size
            avg_points = total_points / batch_size

            if alpha_step > 0 and epoch % alpha_step == 0 and alpha > 0:
                alpha = max(alpha - alpha_decay, 0)

            cls._log(
                f'* Epoch: {epoch:<{epoch_spaces}} '
                f'| Avg L: {avg_loss:<15.8f} '
                f'| Avg R: {avg_reward:<15.8f} '
                f'| Avg P: {avg_points:<15.8f} '
                f'| Alpha: {alpha:<15.8f}'
            )

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


__all__ = ["PeggingTrainerPreLoaded"]
