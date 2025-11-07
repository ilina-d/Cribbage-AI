import random


class CardDeck:
    """ Helper functions for card deck logic. """

    CARD_RANKS = '123456789TJQK'
    CARD_SUITS = 'SDCH'
    CARD_EMOJIS = '♠♦♣♥'


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
        Deal a number of cards from the deck.

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
            The rank (1-13), suit (emoji) and worth (1-10) of the card.
        """

        return CardDeck.get_card_rank(card), CardDeck.get_card_suit(card), CardDeck.get_card_worth(card)


    @staticmethod
    def get_card_worth(card: str) -> int:
        """
        Get the given card's worth.

        ------

        Arguments:
             card: The card in rank-suit format.

        ------

        Returns:
            The worth of the given card.
        """

        rank = CardDeck.get_card_rank(card)
        return rank if rank < 11 else 10


    @staticmethod
    def get_card_rank(card: str) -> int:
        """
        Get the given card's rank.

        ------

        Arguments:
             card: The card in rank-suit format.

        ------

        Returns:
            The rank of the given card.
        """

        return CardDeck.CARD_RANKS.index(card[0]) + 1


    @staticmethod
    def get_card_suit(card: str) -> str:
        """
        Get the given card's suit as an emoji.

        ------

        Arguments:
             card: The card in rank-suit format.

        ------

        Returns:
            The card's suit as an emoji.
        """

        return CardDeck.CARD_EMOJIS[CardDeck.CARD_SUITS.index(card[1])]


__all__ = ["CardDeck"]
