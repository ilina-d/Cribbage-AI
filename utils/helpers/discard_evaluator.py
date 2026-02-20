import itertools

from utils.helpers import CardDeck, Scoring


class DiscardEvaluator:
    """ Helper for discarding cards based on statistical probability. """

    _precomputed_scores: dict[str, int] = {}


    @classmethod
    def _precompute_scores(cls) -> None:
        """ Precompute scores for all possible 5-card hand combinations, ignoring suits. """

        if cls._precomputed_scores:
            return

        for combo in itertools.combinations_with_replacement(CardDeck.CARD_RANKS, 5):
            if any(combo.count(card) > 4 for card in set(combo)):
                continue

            cards = list(combo)
            cls._precomputed_scores[''.join(cards)] = Scoring.score_15(cards, 'hand')[0] + \
                Scoring.score_run(cards, 'hand')[0] + Scoring.score_pair(cards, 'hand')[0]


    @classmethod
    def score_hand(cls, cards: list[str], starter_card: str) -> int:
        """
        Calculate the score of a given hand and starter card using precomputed hand scores.

        ------

        Arguments:
             cards: List of 4 cards in rank-suit format.
             starter_card: The starter card in rank-suit format.

        ------

        Returns:
            The hand's score.
        """

        if not cls._precomputed_scores:
            cls._precompute_scores()

        hand_key = ''.join(sorted([card[0] for card in cards + [starter_card]], key = CardDeck.CARD_RANKS.index))
        score = cls._precomputed_scores[hand_key]

        # Flush
        unique_suits = set([card[1] for card in cards])
        if len(unique_suits) == 1:
            score += 4
            if starter_card[1] in unique_suits:
                score += 1

        # His nobs
        for card in cards:
            if card[0] == 'J' and starter_card[1] == card[1]:
                score += 2
                break

        return score


    @classmethod
    def score_crib(cls, cards: list[str], starter_card: str) -> int:
        """
        Calculate the score of a given crib and starter card using precomputed hand scores.

        ------

        Arguments:
             cards: List of 4 cards in rank-suit format.
             starter_card: The starter card in rank-suit format.

        ------

        Returns:
            The crib's score.
        """

        if not cls._precomputed_scores:
            cls._precompute_scores()

        hand_key = ''.join(sorted([card[0] for card in cards + [starter_card]], key=CardDeck.CARD_RANKS.index))
        score = cls._precomputed_scores[hand_key]

        # Flush
        unique_suits = set([card[1] for card in cards + [starter_card]])
        if len(unique_suits) == 1:
            score += 5

        # His heels
        if starter_card[0] == 'J':
            score += 2

        return score


    @classmethod
    def get_discard_stats(cls, hand: list[str], is_dealer: bool) -> dict[str, list]:
        """
        Get discard suggestions for a given hand.

        ------

        Arguments:
             hand: List of 6 cards in rank-suit format.
             is_dealer: Whether the hand belongs to the dealer.

        ------

        Returns:
            A dictionary of different discard suggestions, sorted from best to worst (by their criteria).
        """

        discard_combos = {}
        deck = CardDeck(shuffle = False)
        deck = [card for card in deck.cards if card not in hand]
        for my_cards in itertools.combinations(hand, 2):
            remaining_hand = [card for card in hand if card not in my_cards]

            all_hand_scores = []
            all_crib_scores = []
            all_disc_scores = []
            for starter_card in deck:

                hand_score = cls.score_hand(remaining_hand, starter_card)
                all_hand_scores.append(hand_score)

                remaining_deck = deck.copy()
                remaining_deck.remove(starter_card)
                for opp_cards in itertools.combinations(remaining_deck, 2):
                    crib_cards = list(my_cards) + list(opp_cards)
                    crib_score = cls.score_crib(crib_cards, starter_card)
                    all_crib_scores.append(crib_score)

                    disc_score = hand_score + crib_score if is_dealer else hand_score - crib_score
                    all_disc_scores.append(disc_score)

            avg_score = sum(all_disc_scores) / len(all_crib_scores)
            min_score = min(all_disc_scores)
            max_score = max(all_disc_scores)
            hand_score = sum(all_hand_scores) / len(all_hand_scores)
            high_score = sorted(all_disc_scores)[int(len(all_disc_scores) * 0.95)]

            discard_combos[my_cards] = {'avg' : avg_score, 'min' : min_score, 'max' : max_score,
                                        'hand' : hand_score, 'high' : high_score}

        # Recommended: Card pairs sorted by the highest average when discarded.
        #              If there are multiple combinations with the same average, take the one with the
        #              highest hand score.
        recommended = [(cards, scores['avg']) for cards, scores in sorted(
            discard_combos.items(), key = lambda item: (item[1]['avg'], item[1]['hand']), reverse = True)]

        # For the following plays, if there are multiple combinations with the same value (min, max, ...),
        # take the one with the highest average.

        # Sure Bet: Card pairs sorted by the highest minimum when discarded.
        sure_bet = [(cards, scores['min']) for cards, scores in sorted(
            discard_combos.items(), key = lambda item: (item[1]['min'], item[1]['avg']), reverse = True)]

        # Risky Bet: Card pairs sorted by the highest maximum when discarded.
        risky_bet = [(cards, scores['max']) for cards, scores in sorted(
            discard_combos.items(), key = lambda item: (item[1]['max'], item[1]['avg']), reverse = True)]

        # Hail Mary: Card pairs sorted by their best shot at a high score when discarded.
        #            Where the high score is X points or more, 5% of the time.
        hail_mary = [(cards, scores['high']) for cards, scores in sorted(
            discard_combos.items(), key = lambda item: (item[1]['high'], item[1]['avg']), reverse = True)]

        # Aggressive: Card pairs sorted by the highest average hand score when discarded.
        aggressive = [(cards, scores['hand']) for cards, scores in sorted(
            discard_combos.items(), key = lambda item: (item[1]['hand'], item[1]['avg']), reverse = True)]


        return {
            'recommended' : recommended,
            'sure_bet' : sure_bet,
            'risky_bet' : risky_bet,
            'hail_mary' : hail_mary,
            'aggressive' : aggressive
        }


__all__ = ['DiscardEvaluator']
