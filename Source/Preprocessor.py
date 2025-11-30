from Data import Data
from Input import Input


class Preprocessor:
    
    def __init__(self):
        pass
           
    # Processes input data coming from the UI and stores it inside of the core
    @staticmethod
    def run_preprocessing(input_data : Input, core):
        
        data : Data = core.data