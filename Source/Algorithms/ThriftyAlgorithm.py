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
    matrix = [[900, 4653456, 3345345],
              [4, 49, 5],
              [534, 50, 1534435]]
    data = Data(n=3, matrix=matrix)
    ThriftyAlgorithm.run(data)

    print(data.statistics.sugarity_data_per_algorithm)
    print(data.matrix)


test()
