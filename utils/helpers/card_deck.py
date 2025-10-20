import random


class CardDeck:
    """ Helper functions for card deck logic. """

    CARD_RANKS = '123456789TJQK'
    CARD_SUITS = 'SDCH'
    CARD_EMOJIS = '♠️♦️♣️♥️'

    def __init__(self, shuffle: bool = True) -> None:
        """
        Create a new deck of cards.

        ------

        Arguments:
            shuffle: Whether to shuffle the deck.
        """

        self.cards = []
        for suit in self.CARD_SUITS:
            for rank in self.CARD_RANKS:
                self.cards.append(f'{rank}{suit}')

        if shuffle:
            random.shuffle(self.cards)


    def deal_cards(self, number_of_cards: int) -> list[str]:
        """
        Deal the number of cards from the deck.

        ------

        Arguments:
            number_of_cards: The number of cards to deal.

        ------

        Returns:
            The list of dealt cards (removed from the deck).
        """

        return [self.cards.pop() for _ in range(number_of_cards)]


    @staticmethod
    def unpack_card(card: str) -> tuple[int, str, int]:
        """
        Get elements of the given card.

        ------

        Arguments:
            card: The card to unpack in rank-suit format.

        ------

        Returns:
            The rank (1-13), suit (emojo-jojo) and worth (1-10) of the card.
        """

        rank = CardDeck.CARD_RANKS.index(card[0]) + 1
        suit = CardDeck.CARD_EMOJIS[CardDeck.CARD_SUITS.index(card[1])]
        worth = rank if rank < 11 else 10

        return rank, suit, worth

__all__=["CardDeck"]