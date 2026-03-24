from utils.helpers import CardDeck


class StateEncoder:
    """ Helper for encoding the game state and its parts into a format recognizable for a neural network. """

    LENGTH_CARD_INPUT = 6
    LENGTH_DISCARD_INPUT = 39
    LENGTH_PEGGING_INPUT = 69


    @classmethod
    def encode_card(cls, card: str) -> list[int]:
        """
        Encode a given card into a format recognizable for a neural network.

        ------

        Arguments:
            card: The card that will be encoded, in rank-suit format.

        ------

        Returns:
            The card encoded in a vector of 6 values (1 integer value for worth, 4 binary values for
            the suit, and one integer value for the rank).
        """

        card_rank = CardDeck.get_card_rank(card)
        card_worth = CardDeck.get_card_worth(card)
        card_suit = card[1]

        card_suit_idx = CardDeck.CARD_SUITS.index(card_suit)

        encoded_card = [0] * 6

        encoded_card[0] = card_worth
        encoded_card[1 + card_suit_idx] = 1
        encoded_card[5] = card_rank

        return encoded_card


    @classmethod
    def encode_state_for_discard_phase(cls, player_score: int, opponent_score: int, is_dealer: bool,
                                       player_hand: list[str]) -> list[float | int]:
        """
        Encode the state during the discard phase into a format recognizable for a neural network.

        ------

        Arguments:
            player_score: The neural network player's score.
            opponent_score: The opponent's score.
            is_dealer: Whether the neural network player is the dealer.
            player_hand: The neural network player's cards in hand.

        ------

        Returns:
            The encoded state in a vector of 39 values (1 float-normalized value for each player's score,
            one binary value indicating the dealer and 6 * 6 values for the players cards in hand).
        """

        player_score_val = min(player_score, 121) / 121
        opponent_score_val = min(opponent_score, 121) / 121

        encoded_state = [player_score_val, opponent_score_val, int(is_dealer)]

        for card in player_hand:
            encoded_card = cls.encode_card(card)
            encoded_state.extend(encoded_card)

        return encoded_state

    @classmethod
    def encode_state_for_pegging_phase(cls, player_score: int, opponent_score: int, current_crib_sum: int,
                                       current_crib_cards: list[str], player_hand: list[str]) -> list[float | int]:
        """
        Encode the state during the pegging phase into a format recognizable for a neural network.

        ------

        Arguments:
            player_score: The neural network player's score.
            opponent_score: The opponent's score.
            current_crib_sum: The total of the current crib.
            current_crib_cards: The played cards in the current crib.
            player_hand: The neural network player's cards in hand.

        ------

        Returns:
            The encoded state in a vector of 69 values (1 float-normalized value for each player's score,
            one integer value for the current crib sum, 7 * 6 values for the cards in the current crib,
            and 4 * 6 values for the players cards in hand).
        """

        player_score_val = min(player_score, 121) / 121
        opponent_score_val = min(opponent_score, 121) / 121
        current_crib_sum_val = current_crib_sum

        encoded_state = [player_score_val, opponent_score_val, current_crib_sum_val]

        for card_idx in range(7):
            if card_idx >= len(current_crib_cards):
                encoded_state.extend([0] * 6)
            else:
                encoded_card = cls.encode_card(current_crib_cards[card_idx])
                encoded_state.extend(encoded_card)

        for card_idx in range(4):
            if card_idx >= len(player_hand):
                encoded_state.extend([0] * 6)
            else:
                encoded_card = cls.encode_card(player_hand[card_idx])
                encoded_state.extend(encoded_card)

        return encoded_state


__all__ = ['StateEncoder']
