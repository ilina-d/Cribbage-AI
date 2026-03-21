from multiprocessing import Pool, cpu_count
import cProfile
import time

from utils.game import Game
from utils.players import BasePlayer, UserPlayer


def _get_game_data(args: dict[str, ...]) -> dict[str, ...]:
    """
    Get data from a full game simulation.

    ------

    Arguments:
         args: A dictionary containing game information.

    ------

    Returns:
        A dictionary with the results and data from the simulation.
    """

    player1, player2, first_dealer = args['player1'], args['player2'], args['first_dealer']

    game = Game(
        player1 = player1, player2 = player2, first_dealer = first_dealer,
        wait_after_move = None, wait_after_info = False,
        show_opponents_hand = False, visuals = False,
        measure_statistics = True
    )

    game_start_time = time.time()
    winner = game.play()
    game_time_taken = time.time() - game_start_time

    return {
        'winner' : 'player1' if winner is player1 else 'player2',
        'time_taken' : game_time_taken,
        'total_rounds' : game.stats_total_game_rounds,
        'avg_score_diff' : sum(game.stats_score_diff) / len(game.stats_score_diff),
        'avg_score_diff_dealer1' : sum(game.stats_score_diff_dealer1) / len(game.stats_score_diff_dealer1),
        'avg_score_diff_dealer2' : sum(game.stats_score_diff_dealer2) / len(game.stats_score_diff_dealer2),
        'first_dealer' : first_dealer
    }



class Simulator:
    """ Game simulations and performance measurements. """

    def __init__(self, player1: BasePlayer, player2: BasePlayer, num_simulations: int,
                 measure_performance: bool = True, num_workers: int = 1) -> None:
        """
        Create a new instance of the DiscardSimulator.

        ------

        Arguments:
            player1: The first player object. Cannot be UserPlayer.
            player2: The second player object. Cannot be UserPlayer.
            num_simulations: Number of simulations to run.
            measure_performance: Whether to measure the performance of the code.
            num_workers: Number of cores to use for simulations.
        """

        if isinstance(player1, UserPlayer) or isinstance(player2, UserPlayer):
            raise Exception('Players cannot be of type UserPlayer when running simulations.')

        self.player1 = player1
        self.player2 = player2
        self.num_simulations = num_simulations
        self.measure_performance = measure_performance
        self.num_workers = min(cpu_count(), num_workers)


    def _run_simulations(self) -> str:
        """
        Run the simulator.

        ------

        Returns:
            Results of the simulations.
        """

        total_sim_time = time.time()
        sum_game_times = 0
        sum_game_rounds = 0
        sum_avg_score_diffs = 0
        sum_avg_score_diffs_d1 = 0
        sum_avg_score_diffs_d2 = 0
        player1_wins, player2_wins = 0, 0
        dealer1_wins, dealer2_wins = 0, 0

        print('[ SIMULATOR ] : Running simulations...', end = '\r')

        with Pool(processes = self.num_workers) as pool:
            _sim_args = []

            _sim_args.extend([{
                'player1' : self.player1, 'player2' : self.player2, 'first_dealer' : 'player1'
            }] * (self.num_simulations // 2))

            _sim_args.extend([{
                'player1' : self.player1, 'player2' : self.player2, 'first_dealer' : 'player2'
            }] * (self.num_simulations - (self.num_simulations // 2)))

            for n, result in enumerate(pool.imap_unordered(_get_game_data, _sim_args), start = 1):
                winner = result['winner']
                sum_game_times += result['time_taken']
                sum_game_rounds += result['total_rounds']
                sum_avg_score_diffs += result['avg_score_diff']
                sum_avg_score_diffs_d1 += result['avg_score_diff_dealer1']
                sum_avg_score_diffs_d2 += result['avg_score_diff_dealer2']

                if winner == 'player1':
                    player1_wins += 1
                    if result['first_dealer'] == 'player1':
                        dealer1_wins += 1
                else:
                    player2_wins += 1
                    if result['first_dealer'] == 'player2':
                        dealer2_wins += 1

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

                print(
                    '\r\033[K'
                    f'[ SIMULATOR ] : Running simulations... '
                    f'{str(round(percent_done, 2)) + "%":<6} '
                    f'<{"=" * int(percent_done)}{"-" * int(100 - int(percent_done))}> '
                    f'| P1 ({player1_wins}) vs ({player2_wins}) P2 '
                    f'| ETL: {estimated_tl}', end = ''
                )

        dealer1_win_percent = dealer1_wins / player1_wins * 100 if player1_wins != 0 else 0
        dealer2_win_percent = dealer2_wins / player2_wins * 100 if player2_wins != 0 else 0

        results = (
            f'\n'
            f'-----[ SIMULATION RESULTS ]-----\n'
            f'[ {self.player1.__class__.__name__} ] vs [ {self.player2.__class__.__name__} ]\n'
            f'=================================================\n'
            f'--- Configuration             :\n'
            f'* Player 1                    : {self.player1.__class__.__name__}\n'
            f'* Player 2                    : {self.player2.__class__.__name__}\n'
            f'* Number of Simulations       : {self.num_simulations}\n'
            f'* Number of Workers           : {self.num_workers}\n'
            f'* Measuring Performance       : {self.measure_performance}\n'
            f'=================================================\n'
            f'--- Duration Stats            :\n'
            f'* Total Simulation Time       : {time.time() - total_sim_time:.2f} sec\n'
            f'* Total Game Time             : {sum_game_times:.2f} sec\n'
            f'* Average Game Time           : {sum_game_times / self.num_simulations:.2f} sec\n'
            f'=================================================\n'
            f'--- Game Conclusion Stats     :\n'
            f'* Player 1 Wins               : {player1_wins} ( {player1_wins / self.num_simulations * 100:.2f}% )\n'
            f'* Player 2 Wins               : {player2_wins} ( {player2_wins / self.num_simulations * 100:.2f}% )\n'
            f'* Player 1 Wins as 1st Dealer : {dealer1_wins} of {player1_wins} ( {dealer1_win_percent:.2f}% )\n'
            f'* Player 2 Wins as 1st Dealer : {dealer2_wins} of {player2_wins} ( {dealer2_win_percent:.2f}% )\n'
            f'* Avg Game Length             : {int(sum_game_rounds / self.num_simulations)} rounds\n'
            f'=================================================\n'
            f'--- Score Difference Stats    :\n'
            f'* Avg Score Diff Overall      : {sum_avg_score_diffs / self.num_simulations:.2f}\n'
            f'* Avg Score Diff (P1 dealer)  : {sum_avg_score_diffs_d1 / self.num_simulations:.2f}\n'
            f'* Avg Score Diff (P2 dealer)  : {sum_avg_score_diffs_d2 / self.num_simulations:.2f}\n'
            f'  [!] score_diff = player1.score - player2.score\n'
            f'=================================================\n'
            f'\n'
        )

        print(results)
        return results


    def start(self) -> str:
        """
        Start the simulator.

        ------

        Returns:
            Results of the simulations.
        """

        if self.measure_performance:
            profile = cProfile.Profile()
            results = profile.runcall(self._run_simulations)
            profile.print_stats()

        else:
            results = self._run_simulations()

        return results


__all__ = ['Simulator']
