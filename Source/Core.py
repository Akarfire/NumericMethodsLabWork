from Data import Data
from Results import Results
from Input import Input

from Preprocessor import Preprocessor
from Solver import Solver
from Postprocessor import Postprocessor
from UserInterface import UserInterface

class Core:
    
    def __init__(self):
        
        # UI server
        # self.ui_server = None
        
        # Modules
        self.preprocessor = Preprocessor()
        self.solver = Solver()
        self.postprocessor = Postprocessor()
        
        self.userInterface = UserInterface(self)
    
    
    def __run_experiment(self, input_data : Input):
        
        data : Data = Data()
        
        for i in range(input_data.experiment_count):
            prep_data = self.preprocessor.run_preprocessing(input_data, self)
            solv_data = self.solver.run_solver(prep_data)
            
            # Merging data
            if i == 0:
                data = solv_data
            else:
                self.__merge_experiment_data(data, solv_data)
            
        results : Results = self.postprocessor.run_postprocessing(data)
        self.__respond_send_results(results)
        
        
    # Merges data from small experiments
    def __merge_experiment_data(self, merge_target : Data, merge_object : Data):
        
        for algorithm, value in merge_object.statistics.sugarity_data_per_algorithm.items():
            
            if not algorithm in merge_target.statistics.sugarity_data_per_algorithm:
                merge_target.statistics.sugarity_data_per_algorithm[algorithm] = list(merge_object.n)
            
            for i, v in enumerate(value):
                merge_target.statistics.sugarity_data_per_algorithm[algorithm][i] += v
            
        
    # UI Interface
    
    def init_ui(self):
        self.userInterface.run_ui()
    
    # Called from the UI side
    def call_run(self, input_data : Input):
        self.__run_experiment(input_data)
        
    # Sends results back to the UI side
    def __respond_send_results(self, results: Results):
        self.userInterface.send_results(results)