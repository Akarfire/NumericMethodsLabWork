from Data import Data


class Preprocessor:
    
    def __init__(self):
        pass
           
    # Processes input data coming from the UI and stores it inside of the core
    @staticmethod
    def run_preprocessing(input_data : dict, core):
        
        data : Data = core.data