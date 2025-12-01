from Data import Data

# Importing algorithms
from Algorithms import ExampleAlgorithm

class Solver:
    
    def __init__(self):
        pass
    
    # Runs algorithms
    @staticmethod
    def run_solver(core):
        
        data : Data = core.data
        
        # Running algorithms
        
        example : ExampleAlgorithm = ExampleAlgorithm()
        example_data : Data = example.run(data)
        
        # Working with obtained data and storing it into core's data
        # core.data = example_data
        
        