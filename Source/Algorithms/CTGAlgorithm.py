from Algorithm import Algorithm
from AlgorithmNames import AlgorithmNames
from Data import Data, Statistics
from copy import copy


class CTGAlgorithm(Algorithm):

    def __init__(self):
        super().__init__()

    # Basic method to be overriden,
    # Changes input data,
    # Returns nothing
    @staticmethod
    def run(input_data: Data) -> None:

        stages = input_data.n
        v = input_data.ctg_stage
        sugarity_per_stage = list()
        indices = list()

        # Filling indices according to formula
        for i in range(v - 1):
            ind = stages - 2 * v + 1 + 2 * (i + 1)
            indices.append(ind - 1)

        for i in range(v - 1, 2 * v - 1):
            ind = stages - 2 * (i - (v - 1))
            indices.append(ind - 1)

        for i in range(2 * v - 1, stages):
            ind = stages - i
            indices.append(ind - 1)

        # Algorithm implementation
        for cur_stage in range(stages):
            max_c = input_data.matrix[indices[cur_stage]][cur_stage]
            if len(sugarity_per_stage) == 0:
                sugarity_per_stage.append(max_c)
            else:
                sugarity_per_stage.append(sugarity_per_stage[-1] + max_c)

        # Add new statistics to input
        input_data.statistics.sugarity_data_per_algorithm[AlgorithmNames.CTG] = sugarity_per_stage


def test():
    matrix = [[1, 1, 1456456, 100, 1],
              [2, 2, 2,       200, 2],
              [3, 3, 3345345, 300, 3],
              [4, 4, 4,       4,   4],
              [5, 5, 5234234, 5,   5]]
    data = Data(n=5, ctg_stage=2, matrix=matrix)
    CTGAlgorithm.run(data)

    print(data.statistics.sugarity_data_per_algorithm)
    prev = 0
    print("Choosing order: ",end="")
    for i in data.statistics.sugarity_data_per_algorithm[AlgorithmNames.CTG]:
        print(i - prev, end=" ")
        prev = i
    print()
    print(data.matrix)


if __name__ == "__main__":
    test()
