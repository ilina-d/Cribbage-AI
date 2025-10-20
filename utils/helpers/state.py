class State:
    """ Representation of game states. ️ """

    points: list[int, int] = [0, 0]
    dealer: ... = None
    starter_card: str = None
    cribs: list[list[str], list[str], list[str]] = [[], [], []]


    def check_win(self) -> None | int:
        """
        Check if there is a winner in the current game state.

        ------

        Returns:
            The index of the winning player, otherwise None.
        """

        if self.points[0] >= 121:
            return 0

        if self.points[1] >= 121:
            return 1

        return None

__all__ = ["State"]