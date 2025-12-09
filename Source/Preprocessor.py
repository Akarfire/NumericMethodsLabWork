from Data import Data
from Input import Input, DegradationMode
import numpy as np

class Preprocessor:
    
    def __init__(self):
        pass
           
    # Processes input data coming from the UI and stores it inside of the core
    @staticmethod
    def run_preprocessing(input_data : Input, core) -> Data:
        
        data : Data = Data()

        data.n = input_data.n
        data.m = input_data.m
        data.experiment_count = input_data.experiment_count

        data.greedy_thrifty_stage = input_data.greedy_thrifty_stage
        data.thrifty_greedy_stage = input_data.thrifty_greedy_stage
        data.bkj_rank = input_data.bkj_rank
        data.bkj_stage = input_data.bkj_stage
        data.ctg_stage = input_data.ctg_stage

        # initial values
        a_values = Preprocessor.generate_initial_values(input_data)
        
        # degradation
        b_matrix = Preprocessor.generate_degradation_values(input_data)

        if (input_data.use_ripening):
            b_matrix = Preprocessor.generate_ripening(input_data, b_matrix)

        c_matrix = Preprocessor.generate_c_matrix(input_data, a_values, b_matrix)   

        if (input_data.use_non_organics):
            c_matrix = Preprocessor.generate_non_organics(input_data, c_matrix)

        # for i in range(input_data.n):
        #     for j in range(input_data.n):
        #         print(f"{c_matrix[i][j]:.3f}", end=" ")
        #     print("\n")

        data.matrix = c_matrix
        
        return data
        

    @staticmethod
    def generate_ripening(input_data : Input, b_matrix):
        if (input_data.degradation_mode == DegradationMode.UNIFORM):
            for i in range(input_data.n):
                for j in range(input_data.ripening_stages):
                    b_matrix[i][j] = np.random.uniform(input_data.ripening_min, input_data.ripening_max)
        else:
            for i in range(input_data.n):
                for j in range(input_data.ripening_stages):
                    delta = (input_data.ripening_max - input_data.ripening_min) * input_data.concentrated_range_fraction
                    right_border = input_data.ripening_max - delta
                    new_min = np.random.uniform(input_data.ripening_min, right_border)
                    b_matrix[i][j] = np.random.uniform(new_min, new_min + delta)
        return b_matrix

    @staticmethod
    def generate_non_organics(input_data : Input, c_matrix):
        k_values = np.random.uniform(input_data.k_min, input_data.k_max, input_data.n)
        na_values = np.random.uniform(input_data.na_min, input_data.na_max, input_data.n)
        n_values = np.random.uniform(input_data.n_min, input_data.n_max, input_data.n)
        reduce_values = np.random.uniform(input_data.reduce_min, input_data.reduce_max, input_data.n)

        reduce_matrix = [[0.0 for _ in range(input_data.n)] for _ in range(input_data.n)]

        for i in range(input_data.n):
            for j in range(input_data.n):
                reduce_matrix[i][j] = reduce_values[i] * ((1.029) ** (7 * j - 7))

        L = [[0.0 for _ in range(input_data.n)] for _ in range(input_data.n)]
        for i in range(input_data.n):
            for j in range(input_data.n):
                L[i][j] = 1.1 + 0.1541 * (k_values[i] + na_values[i]) + 0.2159 * n_values[i] + 0.9989 * reduce_matrix[i][j] + 0.1967
                L[i][j] = L[i][j] / 100

        S = [[0.0 for _ in range(input_data.n)] for _ in range(input_data.n)]
        for i in range(input_data.n):
            for j in range(input_data.n):
                S[i][j] = max(c_matrix[i][j] - L[i][j], 0)
        
        return S

        # TO DO - idk Egor help 

    @staticmethod
    def generate_initial_values(input_data : Input):
        values = [[0.0 for _ in range(input_data.n)] for _ in range(input_data.n)]

        if (input_data.use_individual_ranges):
            for i in range(input_data.n):
                values[i] = np.random.uniform(input_data.individual_a_ranges[i][0], input_data.individual_a_ranges[i][1])
        else:
            values = np.random.uniform(input_data.a_min, input_data.a_max, input_data.n)

        return values
   
    @staticmethod
    def generate_degradation_values(input_data : Input):
        b_matrix = [[0.0 for _ in range(input_data.n)] for _ in range(input_data.n)]
        if (not input_data.use_individual_ranges):
            if (input_data.degradation_mode == DegradationMode.UNIFORM):
                for i in range(input_data.n):
                    for j in range(input_data.n):
                        b_matrix[i][j] = np.random.uniform(input_data.b_min, input_data.b_max)
            else:
                # generate range for each i
                new_b_min = [0.0 for _ in range(input_data.n)]
                delta = (input_data.b_max - input_data.b_min) * input_data.concentrated_range_fraction
                right_border = input_data.b_max - delta
                new_b_min = np.random.uniform(input_data.b_min, right_border, input_data.n)
                
                # generate b_matrix
                for i in range(input_data.n):
                    for j in range(input_data.n):
                        b_matrix[i][j] = np.random.uniform(new_b_min[i], new_b_min[i] + delta)
        else:
            if (input_data.degradation_mode == DegradationMode.UNIFORM):
                for i in range(input_data.n):
                    for j in range(input_data.n):
                        b_matrix[i][j] = np.random.uniform(input_data.individual_b_ranges[i][0], input_data.individual_b_ranges[i][1])
            else:
                # generate range for each i
                new_b_min = [0.0 for _ in range(input_data.n)]
                for i in range(input_data.n):
                    delta = (input_data.individual_b_ranges[i][1] - input_data.individual_b_ranges[i][0]) * input_data.concentrated_range_fraction
                    right_border = input_data.individual_b_ranges[i][1] - delta
                    new_b_min[i] = np.random.uniform(input_data.individual_b_ranges[i][0], right_border, input_data.n)
                
                # generate b_matrix
                for i in range(input_data.n):
                    for j in range(input_data.n):
                        delta = (input_data.individual_b_ranges[i][1] - input_data.individual_b_ranges[i][0]) * input_data.concentrated_range_fraction
                        b_matrix[i][j] = np.random.uniform(new_b_min[i], new_b_min[i] + delta)
        return b_matrix

    def generate_c_matrix(input_data : Input, a_values, b_matrix):
        c_matrix = [[0.0 for _ in range(input_data.n)] for _ in range(input_data.n)]

        for i in range(input_data.n):
            c_matrix[i][0] = a_values[i] 
            for j in range(1, input_data.n):
                c_matrix[i][j] = c_matrix[i][j - 1] * b_matrix[i][j]

        return c_matrix
