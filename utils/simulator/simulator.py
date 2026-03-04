import cProfile
import time

from utils.game import Game
from utils.players import BasePlayer, UserPlayer


class Simulator:
    """ Game simulations and performance measurements. """

    def __init__(self, player1: BasePlayer, player2: BasePlayer,
                 num_simulations: int, measure_performance: bool = True) -> None:
        """
        Create a new instance of the DiscardSimulator.

        ------

        Arguments:
            player1: The first player object. Cannot be UserPlayer.
            player2: The second player object. Cannot be UserPlayer.
            num_simulations: Number of simulations to run.
            measure_performance: Whether to measure the performance of the code.
        """

        if isinstance(player1, UserPlayer) or isinstance(player2, UserPlayer):
            raise Exception('Players cannot be of type UserPlayer when running simulations.')

        self.player1 = player1
        self.player2 = player2
        self.num_simulations = num_simulations
        self.measure_performance = measure_performance


    def _run_simulations(self) -> None:
        """ Run the simulator. """

        total_sim_time = time.time()
        sum_game_times = 0
        sum_game_rounds = 0
        sum_avg_score_diffs = 0
        sum_avg_score_diffs_d1 = 0
        sum_avg_score_diffs_d2 = 0
        player1_wins, player2_wins = 0, 0

        game = Game(
            player1 = self.player1, player2 = self.player2,
            wait_after_move = None, wait_after_info = False,
            show_opponents_hand = False, visuals = False,
            measure_statistics = True
        )

        print('\033[H\033[J', end = '')
        print('[ SIMULATOR ] : Running simulations...')

        for n in range(1, self.num_simulations + 1):
            game_start_time = time.time()
            winner = game.play()

            sum_game_times += time.time() - game_start_time
            sum_game_rounds += game.stats_total_game_rounds
            sum_avg_score_diffs += sum(game.stats_score_diff) / len(game.stats_score_diff)
            sum_avg_score_diffs_d1 += sum(game.stats_score_diff_dealer1) / len(game.stats_score_diff_dealer1)
            sum_avg_score_diffs_d2 += sum(game.stats_score_diff_dealer2) / len(game.stats_score_diff_dealer2)

            if winner is self.player1:
                player1_wins += 1
            else:
                player2_wins += 1

            percent_done = (n / self.num_simulations) * 100
            estimated_tl = (sum_game_times / n) * (self.num_simulations - n)
            if estimated_tl == 0:
                estimated_tl = f'done'
            elif estimated_tl > 3600:
                estimated_tl = f'~{estimated_tl // 3600} hours'
            elif estimated_tl > 60:
                estimated_tl = f'~{estimated_tl // 60} minutes'
            else:
                estimated_tl = f'~{int(estimated_tl)} seconds'

            sims_per_min = n / sum_game_times * 60

            print('\033[H\033[J', end = '')
            print(
                f'[ SIMULATOR ] : Running simulations... '
                f'{str(round(percent_done, 2)) + "%":<6} '
                f'<{"=" * int(percent_done)}{"-" * int(100 - int(percent_done))}> '
                f'| P1 ({player1_wins}) vs ({player2_wins}) P2 '
                f'| ETL: {estimated_tl} '
                f'| ~{sims_per_min:.2f} spm'
            )

        print(
            f'\n'
            f'-----[ SIMULATION RESULTS ]-----\n'
            f'[ {self.player1.__class__.__name__} ] vs [ {self.player2.__class__.__name__} ]\n'
            f'================================================\n'
            f'--- Configuration            :\n'
            f'* Player 1                   : {self.player1.__class__.__name__}\n'
            f'* Player 2                   : {self.player2.__class__.__name__}\n'
            f'* Number of Simulations      : {self.num_simulations}\n'
            f'* Measuring Performance      : {self.measure_performance}\n'
            f'================================================\n'
            f'--- Duration Stats           :\n'
            f'* Total Simulation Time      : {time.time() - total_sim_time:.2f} sec\n'
            f'* Total Game Time            : {sum_game_times:.2f} sec\n'
            f'* Average Game Time          : {sum_game_times / self.num_simulations:.2f} sec\n'
            f'================================================\n'
            f'--- Game Conclusion Stats    :\n'
            f'* Player 1 Wins              : {player1_wins} ({self.player1.__class__.__name__})\n'
            f'* Player 2 Wins              : {player2_wins} ({self.player2.__class__.__name__})\n'
            f'* Avg Game Length            : {int(sum_game_rounds / self.num_simulations)} rounds\n'
            f'================================================\n'
            f'--- Score Difference Stats   :\n'
            f'* Avg Score Diff Overall     : {sum_avg_score_diffs / self.num_simulations:.2f}\n'
            f'* Avg Score Diff (P1 dealer) : {sum_avg_score_diffs_d1 / self.num_simulations:.2f}\n'
            f'* Avg Score Diff (P2 dealer) : {sum_avg_score_diffs_d2 / self.num_simulations:.2f}\n'
            f'  [!] score_diff = player1.score - player2.score\n'
            f'================================================\n'
            f'\n'
        )


    def start(self) -> None:
        """ Start the simulator. """

        if self.measure_performance:
            profile = cProfile.Profile()
            profile.runcall(self._run_simulations)
            profile.print_stats()

        else:
            self._run_simulations()


__all__ = ['Simulator']
