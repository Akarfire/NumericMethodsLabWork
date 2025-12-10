from Algorithm import Algorithm
from AlgorithmNames import AlgorithmNames
from Data import Data, Statistics
from copy import copy


class FastRottingFirstAlgorithm(Algorithm):

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
        # degradation_per_batch[batch]
        degradation_per_batch = list(0.0 for batch in range(stages))

        # Algorithm implementation - at first step we go greedy
        cur_c_list = [input_data.matrix[i][0] for i in batches_left]
        pairs = [(value, original_idx) for value, original_idx in zip(cur_c_list, batches_left)]
        pairs.sort()
        max_c, max_c_ind = pairs[-1]
        sugarity_per_stage.append(max_c)
        batches_left.remove(max_c_ind)

        # Algorithm implementation - thrifty part
        for cur_stage in range(1, stages):
            cur_stage_degrs = list(0.0 for _ in batches_left)

            i = 0
            for batch_ind in batches_left:
                if input_data.matrix[batch_ind][cur_stage - 1] == 0:
                    degradation_per_batch[batch_ind] = float('inf')
                if degradation_per_batch[batch_ind] == float('inf'):
                    pass
                else:
                    degradation_per_batch[batch_ind] += input_data.matrix[batch_ind][cur_stage] /\
                                                        input_data.matrix[batch_ind][cur_stage - 1]
                    cur_stage_degrs[i] = degradation_per_batch[batch_ind] / cur_stage
                i += 1

            # Contains pairs : [batch_degradation, batch_index]
            degradation_index_pairs = [(degr, original_idx) for degr, original_idx in zip(cur_stage_degrs, batches_left)]

            degradation_index_pairs.sort()
            max_deg_c_ind = degradation_index_pairs[0][1]  # берем batch с наибольшей средней деградацией
            max_deg_c = input_data.matrix[max_deg_c_ind][cur_stage]

            if len(sugarity_per_stage) == 0:
                sugarity_per_stage.append(max_deg_c)
            else:
                sugarity_per_stage.append(sugarity_per_stage[-1] + max_deg_c)
            batches_left.remove(max_deg_c_ind)

        # Add new statistics to input
        input_data.statistics.sugarity_data_per_algorithm[AlgorithmNames.FAST_ROTTING_FIRST] = sugarity_per_stage


def test():
    matrix = [[100, 88, 50, 5, 5],
              [100, 70, 10, 200, 2],
              [100, 90, 45, 300, 3],
              [100, 69, 4, 4, 4],
              [100, 1, 1, 1, 1]]
    data = Data(n=5, bkj_rank=2, bkj_stage=3, matrix=matrix)
    FastRottingFirstAlgorithm.run(data)

    print(data.statistics.sugarity_data_per_algorithm)
    prev = 0
    print("Choosing order: ",end="")
    for i in data.statistics.sugarity_data_per_algorithm[AlgorithmNames.FAST_ROTTING_FIRST]:
        print(i - prev, end=" ")
        prev = i
    print()
    print(data.matrix)


if __name__ == "__main__":
    test()
