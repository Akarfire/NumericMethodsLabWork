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
from Algorithms import MinimalAlgorithm
from Algorithms import ThriftyAlgorithm
from Algorithms import RandomAlgorithm


class Solver:

    def __init__(self):
        pass

    # Runs algorithms
    @staticmethod
    def run_solver(in_data: Data) -> Data:
        data: Data = in_data
        algorithms_runs = [
            BkJ.BkJAlgorithm.run,
            CTGAlgorithm.CTGAlgorithm.run,
            GreedyAlgorithm.GreedyAlgorithm.run,
            GreedyThriftyAlgorithm.GreedyThriftyAlgorithm.run,
            HungarianAlgorithm.HungarianAlgorithm.run,
            ThriftyAlgorithm.ThriftyAlgorithm.run,
            ThriftyGreedyAlgorithm.ThriftyGreedyAlgorithm.run,
            MinimalAlgorithm.MinimalAlgorithm.run,
            RandomAlgorithm.RandomAlgorithm.run,
        ]

        # Running algorithms
        for run in algorithms_runs:
            start_time = perf_counter()
            run(data)
            end_time = perf_counter()
            # print(f"{str(run)[10:].split()[0][:-4]} time: {end_time - start_time:.6f} seconds")

        return data


class DataContainer:  # class used for Solver testing
    data: Data
    n : int

    def __init__(self, input_data, n):
        self.data = input_data
        self.n = n


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
                        Solver.run_solver(data)
    print("input ranges test didn't crash")


def testWithEtalons():
    test_small_matrix = [[76, 34, 89, 12, 95],
                         [23, 67, 45, 81,  3],
                         [98, 14, 56, 72, 29],
                         [61,  8, 91, 44, 17],
                         [50, 25, 39, 66, 83]]

    etalons = dict()  # заполняется мной вручную
    etalons[AlgorithmNames.BkJ] = [50, 14, 91, 81, 95]
    etalons[AlgorithmNames.CTG] = [61, 25, 56, 81, 95]
    etalons[AlgorithmNames.GREEDY] = [98, 67, 91, 66, 95]
    etalons[AlgorithmNames.GREEDY_THRIFTY] = [98, 67, 91, 12, 83]
    etalons[AlgorithmNames.HUNGARIAN] = [98, 67, 91, 66, 95]
    etalons[AlgorithmNames.THRIFTY] = [23, 8, 39, 12, 29]
    etalons[AlgorithmNames.THRIFTY_GREEDY] = [23, 8, 89, 72, 83]
    etalons[AlgorithmNames.MINIMAL] = [23, 14, 39, 12, 17]

    data = Data(
        n=len(test_small_matrix),
        bkj_rank=2,
        bkj_stage=3,
        ctg_stage=2,
        greedy_thrifty_stage=4,
        thrifty_greedy_stage=3,
        matrix=test_small_matrix
    )
    Solver.run_solver(data)

    for i in data.statistics.sugarity_data_per_algorithm:
        try:
            actual = list()
            for j in range(len(data.statistics.sugarity_data_per_algorithm[i])):
                if j == 0:
                    actual.append(data.statistics.sugarity_data_per_algorithm[i][j])
                else:
                    cur = data.statistics.sugarity_data_per_algorithm[i][j]
                    prev = data.statistics.sugarity_data_per_algorithm[i][j - 1]
                    actual.append(cur - prev)
            if actual != etalons[i]:
                print("Algorithm doesn't work properly. Breaks on", i)
            else:
                print(i, "works fine")
        except:
            print("It crashes on", i)


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
    Solver.run_solver(data)

    print()

    print("Matrix: ")
    for i in range(len(big_matrix)):
        for j in range(len(big_matrix)):
            print(f"{big_matrix[i][j]:.2f} ", end="")
        print()
    print()

    print("Algorithm results: ")
    for i in data.statistics.sugarity_data_per_algorithm:
        eff = 100.0 * data.statistics.sugarity_data_per_algorithm[i][-1] / \
              data.statistics.sugarity_data_per_algorithm[AlgorithmNames.HUNGARIAN][-1]

        print(f"{i}: {data.statistics.sugarity_data_per_algorithm[i][-1]}. Efficiency: {eff:0.2f}%")


if __name__ == "__main__":
    testWithEtalons()
    test()
    # inputRangesTest()
