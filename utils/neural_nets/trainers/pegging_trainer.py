import random
import copy

import torch
from torch import optim

from utils.neural_nets import BasePeggingNet
from utils.helpers import DiscardEvaluator, CardDeck, Scoring

from multiprocessing import Pool, cpu_count

from utils.players import BasePlayer
from utils.players.dapg_player import DAPGPlayer


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
    player1 = 'Me'
    player2 = opponent
    player2.cards = state['opponent_hand']
    state['dealer'] = player1 if state['is_dealer'] else player2

    current_player = 'Me' if not state['is_dealer'] else opponent
    action_confs, action_scores = [], []
    alpha = state['alpha']

    coach = DAPGPlayer()

    while state['player_hand'] or state['opponent_hand']:
        prev_called_go = called_go
        confidence = None

        if current_player == 'Me':
            current_crib_sum = state['crib_sums'][state['current_crib_idx']]
            current_crib_cards = state['cribs'][state['current_crib_idx']]
            distribution = pegging_net.get_distribution_policy(
                state['score1'], state['score2'], current_crib_sum, current_crib_cards, state['player_hand']
            )

            rely_on_coach = random.choices([True, False], [alpha, 1 - alpha], k=1)[0]
            if rely_on_coach:
                coach.cards = state['player_hand']

                played_card = coach.play_card(state)
                confidence = pegging_net.get_card_confidence(distribution, played_card)
            else:
                log_probs = torch.stack([card[1] for card in distribution])
                probs = torch.exp(log_probs)

                played_card, confidence = distribution[torch.multinomial(probs, 1).item()]

            if played_card != 'GO' and not rely_on_coach:
                state['player_hand'].remove(played_card)
        else:
            played_card = opponent.play_card(state)

        if played_card == 'GO':
            if called_go:
                state['current_crib_idx'] += 1
                called_go = False
            else:
                called_go = True
                if current_player == opponent:
                    state['score1'] += 1
                else:
                    state['score2'] += 1

            if current_player == 'Me':
                action_confs.append(confidence)
                action_scores.append(0)
        else:
            state['cribs'][state['current_crib_idx']].append(played_card)
            score, _ = Scoring.score_card(state, current_player, update_points = False)
            state['crib_sums'][state['current_crib_idx']] += CardDeck.get_card_worth(played_card)

            if current_player == 'Me':
                action_confs.append(confidence)
                action_scores.append(score)
                state['score1'] += score
            else:
                state['score2'] += score

            if state['crib_sums'][state['current_crib_idx']] == 31:
                state['current_crib_idx'] += 1
                called_go = False

        if state['score1'] >= 121 or state['score2'] >= 121:
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
              batch_size: int = 32, pool_size: int = 8, num_workers: int = 1,
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
            num_workers: How many cores to use for training.
            alpha: How reliant the network is on the coach (GreedyPlayer).
            alpha_decay: By how much to reduce the network's dependency on the coach.
            alpha_step: How often to decay alpha in epochs.
            accumulate_loss: Whether to accumulate gradient loss within a batch before stepping.
            inflate_advantage: Whether to inflate the calculated advantage.
 
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

        if pool_size % 5 != 0:
            cls._log(f'Pool size {pool_size} must be a divisible by 5.')
            pool_size = round(pool_size / 5) * 5
            cls._log(f'Pool size changed to {pool_size}.')

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
            f'* Accumulate loss: {accumulate_loss}\n'
            f'* Inflated advantage: {inflate_advantage}\n'
            f'\n'
            f'* Supervised: {alpha > 0}\n'
            f'* Alpha: {alpha}\n'
            f'* Alpha Decay: {alpha_decay}\n'
            f'* Alpha Step: {alpha_step}\n\n'
        )

        cls._log(f'Training with {pegging_network.device}...')
        net.train()

        with Pool(processes = num_workers) as pool:
            num_40p = int(0.4 * pool_size) * epochs
            num_20p = int(0.2 * pool_size) * epochs
            batch_data_args = [{'play_style': ps} for ps in ('recommended', 'aggressive')] * num_40p
            batch_data_args += [{'play_style': 'sure_bet'}] * num_20p
            state_pool_generator = pool.imap_unordered(_get_batch_data, batch_data_args, chunksize=pool_size)

            for epoch in range(1, epochs + 1):
                total_loss, total_reward, total_points = 0, 0, 0

                if accumulate_loss:
                    optimizer.zero_grad()

                state_pool = [next(state_pool_generator) for _ in range(pool_size)]

                for _ in range(batch_size):
                    state = random.choice(state_pool)
                    state = copy.deepcopy(state)
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


__all__ = ["PeggingTrainer"]
