from Data import Data
from Results import Results
from Input import Input

from Preprocessor import Preprocessor
from Solver import Solver
from Postprocessor import Postprocessor

class Core:
    
    def __init__(self):
        
        # UI server
        # self.ui_server = None
        
        # Modules
        self.preprocessor = Preprocessor()
        self.solver = Solver()
        self.postprocessor = Postprocessor()
        
        # Run time data
        self.data : Data = Data()
    
    
    def __run_experiment(self, input_data : Input):
        
        self.preprocessor.run_preprocessing(input_data, self)
        self.solver.run_solver(self)
        results : Results = self.postprocessor.run_postprocessing(self)
        
        self.__respond_send_results(results)
    
        
    # UI Interface
    
    # Called from the UI side
    def call_run(self, input_data_dict : dict):
        
        input_data : Input = Input() # TO DO : Convert input_data_dict to Input
        self.__run_experiment(input_data)
        
    # Sends results back to the UI side
    def __respond_send_results(self, results: Results):
        
        # results.dict()
        pass