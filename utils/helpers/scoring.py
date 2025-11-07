from itertools import combinations

from utils.players import BasePlayer
from utils.helpers import CardDeck


class Scoring:
    """ Calculating card combination scores. """

    @staticmethod
    def score_card(state: dict[str, ...], player: BasePlayer, update_points: bool = False) -> tuple[int, list[str]]:
        """
        Calculate score of the last played card.

        ------

        Arguments:
             state: The game state.
             player: The player whose turn it is.
             update_points: Whether to update the player's points or just return them.

        ------

        Returns:
            The total score along with a list of all tricks scored.
        """

        total_score = 0
        tricks = []
        cards = state['cribs'][state['current_crib_idx']]

        score, info = Scoring.score_15(cards, option = 'play')
        total_score += score
        tricks.extend(info)

        score, info = Scoring.score_run(cards, option = 'play')
        total_score += score
        tricks.extend(info)

        score, info = Scoring.score_pair(cards, option = 'play')
        total_score += score
        tricks.extend(info)

        score, info = Scoring.score_31(cards)
        total_score += score
        tricks.extend(info)

        score, info = Scoring.score_last(state, player, update_points = False)
        total_score += score
        tricks.extend(info)

        if update_points:
            player.points += total_score

        return total_score, tricks


    @staticmethod
    def score_hand(state: dict[str, ...], player: BasePlayer, update_points: bool = False) -> tuple[int, list[str]]:
        """
        Calculate score for the player's hand.

        ------

        Arguments:
            state: The game state.
            player: The player whose hand is being scored.
            update_points: Whether to update the player's points or just return them.

        ------

        Returns:
            The total score along with a list of all tricks scored.
        """

        total_score = 0
        tricks = []
        hand = player.cards
        cards = hand + [state['starter_card']]

        score, info = Scoring.score_15(cards, option = 'hand')
        total_score += score
        tricks.extend(info)

        score, info = Scoring.score_run(cards, option = 'hand')
        total_score += score
        tricks.extend(info)

        score, info = Scoring.score_pair(cards, option = 'hand')
        total_score += score
        tricks.extend(info)

        score, info = Scoring.score_flush(hand, option = 'hand')
        total_score += score
        tricks.extend(info)

        score, info = Scoring.score_nobs(state, player, update_points = False)
        total_score += score
        tricks.extend(info)

        if update_points:
            player.points += total_score

        return total_score, tricks


    @staticmethod
    def score_crib(state: dict[str, ...], crib: list[str], update_points: bool = False) -> tuple[int, list[str]]:
        """
        Calculate score for the dealer's crib.

        ------

        Arguments:
             state: The game state.
             crib: The dealer's crib as a sequence of cards in rank-suit format.
             update_points: Whether to update the dealer's points or just return them.

        ------

        Returns:
            The total score along with a list of all tricks scored.
        """

        player = state['dealer']

        total_score = 0
        tricks = []
        cards = crib + [state['starter_card']]

        score, info = Scoring.score_15(cards, option = 'crib')
        total_score += score
        tricks.extend(info)

        score, info = Scoring.score_run(cards, option = 'crib')
        total_score += score
        tricks.extend(info)

        score, info = Scoring.score_pair(cards, option = 'crib')
        total_score += score
        tricks.extend(info)

        score, info = Scoring.score_flush(cards, option = 'crib')
        total_score += score
        tricks.extend(info)

        if update_points:
            player.points += total_score

        return total_score, tricks


    @staticmethod
    def score_heels(state: dict[str, ...], update_points: bool = False) -> tuple[int, list[str]]:
        """
        Calculate score for the dealer if the starter card is a Jack.

        ------

        Arguments:
             state: The game state.
             update_points: Whether to update the dealer's points or just return them.

        ------

        Returns:
            The total score along with a list of all tricks scored.
        """

        if state['starter_card'][0] != 'J':
            return 0, []

        if update_points:
            state['dealer'].points += 2

        return 2, ['2 for his heels']


    @staticmethod
    def score_go(state: dict[str, ...], player: BasePlayer, update_points: bool = False) -> tuple[int, list[str]]:
        """
        Calculate score for the opposite player of the one who called "GO".

        ------

        Arguments:
             state: The game state.
             player: The player who called "GO".
             update_points: Whether to update the player's points or just return them.

        ------

        Returns:
            The total score along with a list of all tricks scored.
        """

        other_player = state['player1'] if player == state['player2'] else state['player2']
        if update_points:
            other_player.points += 1

        return 1, ['1 for GO']


    @staticmethod
    def score_nobs(state: dict[str, ...], player: BasePlayer, update_points: bool = False) -> tuple[int, list[str]]:
        """
        Calculate score for the player's if there's a Jack of the same suit as the starter card in their hand.

        ------

        Arguments:
            state: The game state.
            player: The player whose hand is being scored.
            update_points: Whether to update the player's points or just return them.

        ------

        Returns:
            The total score along with a list of all tricks scored.
        """

        starter_card = state['starter_card']

        for card in player.cards:
            if card[0] == 'J' and card[1] == starter_card[1]:

                if update_points:
                    player.points += 2

                return 2, [f'2 for his nob [{card} {starter_card}]']

        return 0, []


    @staticmethod
    def score_last(state: dict[str, ...], player: BasePlayer, update_points: bool = False) -> tuple[int, list[str]]:
        """
        Calculate score for the player if they played the last (8th) card.

        ------

        Arguments:
            state: The game state.
            player: The player who played the last card.
            update_points: Whether to update the player's points or just return them.

        ------

        Returns:
            The total score along with a list of all tricks scored.
        """

        if state['crib_sums'][state['current_crib_idx']] == 31:
            return 0, []

        if len(state['cribs'][0]) + len(state['cribs'][1]) + len(state['cribs'][2]) != 8:
            return 0, []

        if update_points:
            player.points += 1

        return 1, ['Last card for 1']


    @staticmethod
    def score_15(cards: list[str], option: str) -> tuple[int, list[str]]:
        """
        Option "play": Calculate score if the given sequence sums up to 15.

        Option "hand" or "crib": Calculate score for all sub-sequences of cards that sum up to 15.

        ------

        Arguments:
            cards: A sequence of cards in rank-suit format.
            option: What is being scored ("play", "hand", "crib").

        ------

        Returns:
            The total score along with a list of all tricks scored.
        """

        cards_worths = [CardDeck.get_card_worth(card) for card in cards]

        if option == 'play':
            if sum(cards_worths) == 15:
                return 2, ['15 for 2']

            return 0, []

        combos = []
        for combo_len in range(2, 6):
            for combo in combinations(zip(cards, cards_worths), combo_len):

                combo_cards, combo_worths = zip(*combo)
                if sum(combo_worths) != 15:
                    continue

                combo_cards = ' '.join(combo_cards)
                combos.append(f'15 for 2 [{combo_cards}]')

        return len(combos) * 2, combos


    @staticmethod
    def score_31(cards: list[str]) -> tuple[int, list[str]]:
        """
        Calculate score if the given sequence sums up to 31.

        ------

        Arguments:
            cards: A sequence of cards in rank-suit format.

        ------

        Returns:
            The total score along with a list of all tricks scored.
        """

        if sum([CardDeck.get_card_worth(card) for card in cards]) == 31:
            return 2, ['31 for 2']

        return 0, []


    @staticmethod
    def score_pair(cards: list[str], option: str) -> tuple[int, list[str]]:
        """
        Option "play": Calculate score if the last card starts or continues a pair.

        Option "hand" or "crib": Calculate score for all sub-sequences of cards that create pairs.

        ------

        Arguments:
            cards: A sequence of cards in rank-suit format.
            option: What is being scored ("play", "hand", "crib").

        ------

        Returns:
            The total score along with a list of all tricks scored.
        """

        if len(cards) < 2:
            return 0, []

        if option == 'play':
            card_rank = cards[-1][0]
            pair_len = 1

            for card in cards[-2 :: -1]:
                if card[0] != card_rank:
                    break
                pair_len += 1

            if pair_len < 2:
                return 0, []

            points = pair_len * (pair_len - 1)
            return points, [f'Pair of {pair_len} for {points}']

        cards_ranks = [card[0] for card in cards]
        points, pairs = 0, []

        for rank in set(cards_ranks):
            pair_len = cards_ranks.count(rank)
            if pair_len < 2:
                continue

            pair = ' '.join([card for card in cards if card[0] == rank])
            pair_points = pair_len * (pair_len - 1)

            points += pair_points
            pairs.append(f'Pair of {pair_len} for {pair_points} [{pair}]')

        return points, pairs


    @staticmethod
    def score_run(cards: list[str], option: str) -> tuple[int, list[str]]:
        """
        Option "play": Calculate score if the last card starts or continues a run.

        Option "hand" or "crib": Calculate score for all sub-sequences of cards that create runs.

        ------

        Arguments:
            cards: A sequence of cards in rank-suit format.
            option: What is being scored ("play", "hand", "crib").

        ------

        Returns:
            The total score along with a list of all tricks scored.
        """

        cards_len = len(cards)
        if cards_len < 3:
            return 0, []

        cards_ranks = [CardDeck.get_card_rank(card) for card in cards]

        if option == 'play':
            for run_len in range(cards_len, 2, -1):

                unique_ranks = set()
                for rank in cards_ranks[:cards_len - run_len:-1]:
                    if rank in unique_ranks:
                        break
                    unique_ranks.add(rank)

                if len(unique_ranks) < 3:
                    break

                if max(unique_ranks) - min(unique_ranks) == len(unique_ranks) - 1:
                    return run_len, [f'Run of {run_len} for {run_len}']

            return 0, []

        cards_ranks.sort()
        unique_ranks = list(set(cards_ranks))
        unique_ranks_len = len(unique_ranks)
        if unique_ranks_len < 3:
            return 0, []

        for run_len in range(unique_ranks_len, 2, -1):
            for start in range(unique_ranks_len - run_len + 1):

                combo = unique_ranks[start: start + run_len]
                if combo[-1] - combo[0] == run_len - 1:
                    run = ' '.join([card for card in cards if CardDeck.get_card_rank(card) in combo])
                    num_duplicates = sum([cards_ranks.count(rank) - 1 for rank in combo]) + 1
                    points = run_len * num_duplicates
                    return points, [f'Run of {run_len} for {points} [{run}]']

        return 0, []


    @staticmethod
    def score_flush(cards: list[str], option: str) -> tuple[int, list[str]]:
        """
        Option "play": Does nothing.

        Option "hand": Calculate score if all cards are of the same suit. Assumes there are 4 cards given.

        Option "card": Calculate score if all cards are of the same suit. Assumes there are 5 cards given.

        ------

        Arguments:
            cards: A sequence of cards in rank-suit format.
            option: What is being scored ("play", "hand", "crib").

        ------

        Returns:
            The total score along with a list of all tricks scored.
        """

        if option == 'play':
            return 0, []

        unique_suits = set([card[1] for card in cards])
        unique_suits_len = len(unique_suits)

        if unique_suits_len == 1:
            flush = ' '.join(cards)
            return unique_suits_len, [f'Flush of {unique_suits_len} for {unique_suits_len} [{flush}]']

        return 0, []


__all__ = ['Scoring']
