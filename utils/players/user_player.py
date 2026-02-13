from .base_player import BasePlayer


class UserPlayer(BasePlayer):
    """ Player agent controlled by the user. """

    def discard_cards(self, state: dict[str, ...]) -> list[str]:

        valid_moves = list(range(1, 7))

        while True:
            idxs = input('Choose two indexes of cards to discard (1, 2, ...): \033[0J').strip().split(' ')

            if len(idxs) != 2 or idxs[0] == idxs[1] or not idxs[0].isdigit() or not idxs[1].isdigit():
                print("Input must be two different indexes... 🙄", end = ' ')
                continue

            idx1, idx2 = int(idxs[0]), int(idxs[1])

            if idx1 < idx2:
                idx1, idx2 = idx2, idx1

            if idx1 in valid_moves and idx2 in valid_moves:
                return [self.cards.pop(idx1 - 1), self.cards.pop(idx2 - 1)]

            print("Invalid choice... 🙄", end=' ')


    def play_card(self, state: dict[str, ...]) -> str:

        valid_moves = self.get_valid_moves(state)
        valid_moves_len = len(valid_moves)

        if valid_moves == ['GO']:
            input('Only valid move is "GO", press enter to continue...\033[0J')
            return "GO"

        while True:
            idx = input('Choose the index of the card to play (1, 2, ...): \033[0J')

            if not idx.isdigit() or int(idx) > valid_moves_len:
                print("Invalid choice... 🙄", end = ' ')
                continue

            return self.cards.pop(int(idx) - 1)


__all__ = ['UserPlayer']
