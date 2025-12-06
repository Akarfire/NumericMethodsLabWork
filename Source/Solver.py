from time import perf_counter
from random import uniform
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
    def run_solver(core):
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
            #print(f"{str(run)[10:].split()[0][:-4]} time: {end_time - start_time:.6f} seconds")


class DataContainer:  # class used for Solver testing
    data: Data

    def __init__(self, input_data):
        self.data = input_data


def test():
    small_matrix = [[1, 1, 1456456, 100, 1],
                    [2, 2, 2,       200, 2],
                    [3, 3, 3345345, 300, 3],
                    [4, 4, 4,       4,   4],
                    [5, 5, 5234234, 5,   5]]

    big_matrix = list()
    for i in range(15):
        big_matrix.append([])
        for j in range(15):
            big_matrix[i].append(uniform(0.0, 1.0))

    data = Data(
        n=len(big_matrix),
        bkj_rank=4,
        bkj_stage=7,
        ctg_stage=4,
        greedy_thrifty_stage=7,
        thrifty_greedy_stage=7,
        matrix=big_matrix
    )
    dataContainer = DataContainer(data)
    Solver.run_solver(dataContainer)
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
