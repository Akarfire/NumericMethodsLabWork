from time import perf_counter
from random import uniform
from math import floor
from Data import Data
from AlgorithmNames import AlgorithmNames

# Importing algorithms
from Algorithms import HungarianAlgorithm
from Algorithms import GreedyAlgorithm
from Algorithms import ThriftyGreedyAlgorithm
from Algorithms import BkJ
from Algorithms import CTGAlgorithm
from Algorithms import GreedyThriftyAlgorithm
from Algorithms import ThriftyAlgorithm


class Solver:

    def __init__(self):
        pass

    # Runs algorithms
    @staticmethod
    def run_solver(core, show_time=False):
        data: Data = core.data
        algorithms_runs = [
            BkJ.BkJAlgorithm.run,
            CTGAlgorithm.CTGAlgorithm.run,
            GreedyAlgorithm.GreedyAlgorithm.run,
            GreedyThriftyAlgorithm.GreedyThriftyAlgorithm.run,
            HungarianAlgorithm.HungarianAlgorithm.run,
            ThriftyAlgorithm.ThriftyAlgorithm.run,
            ThriftyGreedyAlgorithm.ThriftyGreedyAlgorithm.run,
        ]

        # Running algorithms
        for run in algorithms_runs:
            start_time = perf_counter()
            run(data)
            end_time = perf_counter()
            if show_time:
                print(f"{str(run)[10:].split()[0][:-4]} time: {end_time - start_time:.6f} seconds")


class DataContainer:  # class used for Solver testing
    data: Data

    def __init__(self, input_data):
        self.data = input_data


# input ranges test: (если упадет значит указанные range в Input.py неверные)
def inputRangesTest():
    big_matrix = list()
    n = 15
    for i in range(n):
        big_matrix.append([])
        for j in range(n):
            big_matrix[i].append(uniform(0.0, 1.0))

    # input ranges test: (если упадет значит указанные range в Input.py неверные)
    for _greedy_thrifty_stage in range(2, floor(n / 2) + 1):
        for _thrifty_greedy_stage in range(2, floor(n / 2) + 1):
            for _bkj_stage in range(1, n + 1):
                for _bkj_rank in range(1, n - _bkj_stage + 1 + 1):
                    for _ctg_stage in range(2, floor(n / 2) + 1):
                        data = Data(
                            n=len(big_matrix),
                            bkj_rank=_bkj_rank,
                            bkj_stage=_bkj_stage,
                            ctg_stage=_ctg_stage,
                            greedy_thrifty_stage=_greedy_thrifty_stage,
                            thrifty_greedy_stage=_thrifty_greedy_stage,
                            matrix=big_matrix
                        )
                        dataContainer = DataContainer(data)
                        Solver.run_solver(dataContainer)
    print("input ranges test didn't crash")


def test():
    small_matrix = [[1, 1, 1456456, 100, 1],
                    [2, 2, 2, 200, 2],
                    [3, 3, 3345345, 300, 3],
                    [4, 4, 4, 4, 4],
                    [5, 5, 5234234, 5, 5]]

    big_matrix = list()
    n = 15
    for i in range(n):
        big_matrix.append([])
        for j in range(n):
            big_matrix[i].append(uniform(0.0, 1.0))

    data = Data(
        n=len(big_matrix),
        bkj_rank=5,
        bkj_stage=5,
        ctg_stage=5,
        greedy_thrifty_stage=5,
        thrifty_greedy_stage=5,
        matrix=big_matrix
    )
    dataContainer = DataContainer(data)
    Solver.run_solver(dataContainer, show_time=True)

    print()

    print("Matrix: ")
    for i in range(len(big_matrix)):
        for j in range(len(big_matrix)):
            print(f"{big_matrix[i][j]:.2f} ", end="")
        print()
    print()

    print("Algorithm results: ")
    for i in dataContainer.data.statistics.sugarity_data_per_algorithm:
        eff = 100.0 * dataContainer.data.statistics.sugarity_data_per_algorithm[i][-1] / \
              dataContainer.data.statistics.sugarity_data_per_algorithm[AlgorithmNames.HUNGARIAN][-1]

        print(f"{i}: {dataContainer.data.statistics.sugarity_data_per_algorithm[i][-1]}. Efficiency: {eff:0.2f}%")


if __name__ == "__main__":
    test()
    inputRangesTest()
