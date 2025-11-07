from .base_player import BasePlayer


class UserPlayer(BasePlayer):
    """ Player agent controlled by the user. """

    def discard_cards(self, state: dict[str, ...]) -> list[str]:

        cards = []

        while True:
            cards = input('Choose two cards to discard (rank-suit format):'
                          '\n> ').split(' ')

            if len(cards) != 2:
                print("Input must be two cards... 🙄")
                continue

            if cards[0] in self.cards and cards[1] in self.cards:
                self.cards.remove(cards[0])
                self.cards.remove(cards[1])
                break

            print("Invalid choice... 🙄")

        return cards


    def play_card(self, state: dict[str, ...]) -> str:

        valid_moves = self.get_valid_moves(state)
        card = ''

        while True:
            card = input('Choose card from hand to play (rank-suit format) or "GO":'
                         '\n> ')

            if card not in valid_moves:
                print("Invalid choice... 🙄")
                continue

            if card != "GO":
                self.cards.remove(card)
            break

        return card


__all__ = ['UserPlayer']