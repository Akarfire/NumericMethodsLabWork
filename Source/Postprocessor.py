from Data import Data
from Results import Results
from AlgorithmNames import AlgorithmNames

class Postprocessor:
    
    def __init__(self):
        pass
    
    # Processes data in the core and converts it into a results strucutre
    @staticmethod
    def run_postprocessing(data : Data) -> Results:
        
        algorithm_name_conversion = {
            AlgorithmNames.GREEDY : "Жадный",
            AlgorithmNames.THRIFTY : "Бережливый",
            AlgorithmNames.GREEDY_THRIFTY : "Жадно-Бережливый",
            AlgorithmNames.THRIFTY_GREEDY : "Бережливо-Жадный",
            AlgorithmNames.BkJ : "БКЖ",
            AlgorithmNames.CTG : "CTG",
            AlgorithmNames.HUNGARIAN : "Венгерский",
            AlgorithmNames.MINIMAL : "Минимальный"
        }
           
        results : Results = Results()
        
        statistics_list = []
        
        for algorithm in data.statistics.sugarity_data_per_algorithm:
            statistics_list.append([algorithm_name_conversion[algorithm], 
                                    data.statistics.sugarity_data_per_algorithm[algorithm][data.n - 1] / data.experiment_count])
            
        statistics_list.sort(key=lambda x: x[1])
        statistics_list.reverse()
        
        results.statistics_list = statistics_list
        
        # Finding best and worst strategies
        
        min_value = 10e10
        max_value = -1.0

        for algorithm, value in statistics_list:
            
            if algorithm == "Венгерский": continue
            if algorithm == "Минимальный": continue
            
            if value > max_value:
                results.best_strategy = algorithm
                max_value = value
                
            if value < min_value:
                results.worst_strategy = algorithm
                min_value = value
        
        # Processing statistics for the plot
        
        for algorithm in data.statistics.sugarity_data_per_algorithm:
            results.statistics[algorithm_name_conversion[algorithm]] = [i / data.experiment_count * data.m for i in data.statistics.sugarity_data_per_algorithm[algorithm]]
        
        return results
        