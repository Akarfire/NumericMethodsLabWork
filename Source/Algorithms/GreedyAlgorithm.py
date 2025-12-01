from Algorithm import Algorithm
from AlgorithmNames import AlgorithmNames
from Data import Data, Statistics
from copy import copy


class GreedyAlgorithm(Algorithm):

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
            max_c = input_data.matrix[batches_left[0]][cur_stage]
            max_ind = batches_left[0]
            for ind in batches_left:
                cur_c = input_data.matrix[ind][cur_stage]
                if cur_c > max_c:
                    max_ind = ind
                    max_c = cur_c
            if len(sugarity_per_stage) == 0:
                sugarity_per_stage.append(max_c)
            else:
                sugarity_per_stage.append(sugarity_per_stage[-1] + max_c)
            batches_left.remove(max_ind)

        # Add new statistics to input
        input_data.statistics.sugarity_data_per_algorithm[AlgorithmNames.GREEDY] = sugarity_per_stage


def test():
    matrix = [[900, 4653456, 3345345],
              [4,   49,      5],
              [534, 50,      1534435]]
    data = Data(n=3, matrix=matrix)
    GreedyAlgorithm.run(data)

    print(data.statistics.sugarity_data_per_algorithm)
    print(data.matrix)


test()
