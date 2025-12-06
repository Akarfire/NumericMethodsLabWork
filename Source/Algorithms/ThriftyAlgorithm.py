from Algorithm import Algorithm
from AlgorithmNames import AlgorithmNames
from Data import Data, Statistics
from copy import copy


class ThriftyAlgorithm(Algorithm):

    def __init__(self):
        super().__init__()

    # Basic method to be overriden,
    # Changes input data,
    # Returns nothing
    @staticmethod
    def run(input_data: Data) -> None:

        stages = input_data.n
        sugarity_per_stage = list()
        batches_left = list(range(0, stages))

        # Algorithm implementation
        for cur_stage in range(stages):
            min_c = input_data.matrix[batches_left[0]][cur_stage]
            min_ind = batches_left[0]
            for ind in batches_left:
                cur_c = input_data.matrix[ind][cur_stage]
                if cur_c < min_c:
                    min_ind = ind
                    min_c = cur_c
            if len(sugarity_per_stage) == 0:
                sugarity_per_stage.append(min_c)
            else:
                sugarity_per_stage.append(sugarity_per_stage[-1] + min_c)
            batches_left.remove(min_ind)

        # Add new statistics to input
        input_data.statistics.sugarity_data_per_algorithm[AlgorithmNames.THRIFTY] = sugarity_per_stage


def test():
    matrix = [[1, 1, 1456456, 100, 1],
              [2, 2, 2,       200, 2],
              [3, 3, 3345345, 300, 3],
              [4, 4, 4,       4,   4],
              [5, 5, 5234234, 5,   5]]
    data = Data(n=5, matrix=matrix)
    ThriftyAlgorithm.run(data)

    print(data.statistics.sugarity_data_per_algorithm)
    prev = 0
    print("Choosing order: ",end="")
    for i in data.statistics.sugarity_data_per_algorithm[AlgorithmNames.THRIFTY]:
        print(i - prev, end=" ")
        prev = i
    print()
    print(data.matrix)


if __name__ == "__main__":
    test()
