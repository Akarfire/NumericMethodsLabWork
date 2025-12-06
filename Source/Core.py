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
        
        # Run time data
        self.data : Data = Data()
        
        self.userInterface = UserInterface(self)
    
    
    def __run_experiment(self, input_data : Input):
        
        self.preprocessor.run_preprocessing(input_data, self)
        self.solver.run_solver(self)
        results : Results = self.postprocessor.run_postprocessing(self)
        
        self.__respond_send_results(results)
    
        
    # UI Interface
    
    def init_ui(self):
        self.userInterface.run_ui()
    
    # Called from the UI side
    def call_run(self, input_data : Input):
        self.__run_experiment(input_data)
        
    # Sends results back to the UI side
    def __respond_send_results(self, results: Results):
        self.userInterface.send_results(results)