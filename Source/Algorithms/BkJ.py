from Algorithm import Algorithm
from AlgorithmNames import AlgorithmNames
from Data import Data, Statistics
from copy import copy


class BkJAlgorithm(Algorithm):

    def __init__(self):
        super().__init__()

    # Basic method to be overriden,
    # Changes input data,
    # Returns nothing
    @staticmethod
    def run(input_data: Data) -> None:

        stages = input_data.n
        thrifty_stages = input_data.bkj_stage - 1
        k = input_data.bkj_rank
        sugarity_per_stage = list()
        batches_left = list(range(0, stages))

        # Algorithm implementation - thrifty part
        for cur_stage in range(thrifty_stages):
            cur_c_list = [input_data.matrix[i][cur_stage] for i in batches_left]
            pairs = [(value, original_idx) for value, original_idx in zip(cur_c_list, batches_left)]
            pairs.sort()
            min_k_c_ind = pairs[k - 1][1]
            min_k_c = input_data.matrix[min_k_c_ind][cur_stage]

            if len(sugarity_per_stage) == 0:
                sugarity_per_stage.append(min_k_c)
            else:
                sugarity_per_stage.append(sugarity_per_stage[-1] + min_k_c)
            batches_left.remove(min_k_c_ind)

        # Algorithm implementation - greedy part
        for cur_stage in range(thrifty_stages, stages):
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
        input_data.statistics.sugarity_data_per_algorithm[AlgorithmNames.BkJ] = sugarity_per_stage


def test():
    matrix = [[1, 1, 1456456, 100, 1],
              [2, 2, 2, 200, 2],
              [3, 3, 3345345, 300, 3],
              [4, 4, 4, 4, 4],
              [5, 5, 5234234, 5, 5]]
    data = Data(n=5, bkj_rank=2, bkj_stage=3, matrix=matrix)
    BkJAlgorithm.run(data)

    print(data.statistics.sugarity_data_per_algorithm)
    print(data.matrix)


test()
