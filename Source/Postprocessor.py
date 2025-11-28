from Data import Data
from Results import Results

class Postprocessor:
    
    def __init__(self):
        pass
    
    # Processes data in the core and converts it into a results strucutre
    @staticmethod
    def run_postprocessing(core) -> Results:
        
        data : Data = core.data      
        results : Results = Results
        
        return results
        