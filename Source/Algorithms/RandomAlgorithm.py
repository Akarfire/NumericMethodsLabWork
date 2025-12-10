from Algorithm import Algorithm
from AlgorithmNames import AlgorithmNames
from Data import Data, Statistics
from random import shuffle


class RandomAlgorithm(Algorithm):

    def __init__(self):
        super().__init__()

    # Basic method to be overriden,
    # Changes input data,
    # Returns nothing
    @staticmethod
    def run(input_data: Data) -> None:

        stages = input_data.n
        sugarity_per_stage = list()

        # Transpose the matrix for linear_sum_assignment
        transposed_matrix = list()
        for i in range(stages):
            transposed_matrix.append(list())
            for j in range(stages):
                transposed_matrix[i].append(input_data.matrix[j][i])

        # Algorithm implementation
        row_ind = [i for i in range(input_data.n)]
        shuffle(row_ind)

        # Filling statistics
        for cur_stage in range(stages):
            cur_c = transposed_matrix[row_ind[cur_stage]][cur_stage]
            if len(sugarity_per_stage) == 0:
                sugarity_per_stage.append(cur_c)
            else:
                sugarity_per_stage.append(sugarity_per_stage[-1] + cur_c)

        # Add new statistics to input
        input_data.statistics.sugarity_data_per_algorithm[AlgorithmNames.RANDOM] = sugarity_per_stage


def test():
    matrix = [[1, 1, 1456456, 100, 1],
              [2, 2, 2,       200, 2],
              [3, 3, 3345345, 300, 3],
              [4, 4, 4,       4,   4],
              [5, 5, 5234234, 5,   5]]
    data = Data(n=5, matrix=matrix)
    RandomAlgorithm.run(data)

    print(data.statistics.sugarity_data_per_algorithm)
    prev = 0
    print("Choosing order: ",end="")
    for i in data.statistics.sugarity_data_per_algorithm[AlgorithmNames.RANDOM]:
        print(i - prev, end=" ")
        prev = i
    print()
    print(data.matrix)


if __name__ == "__main__":
    test()
