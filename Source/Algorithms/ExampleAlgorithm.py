from Algorithm import Algorithm
from Data import Data, Statistics
from copy import copy

class ExampleAlgorithm(Algorithm):
    
    def __init__(self):
        super().__init__()
       
    # Basic method to be overriden,
    # Does not change input data,
    # Returns updated data 
    def run(input_data : Data) -> Data:
        
        new_data : Data = copy(input_data)
        
        # Modifies data somehow
        # new_data.matrix = list()
        
        return new_data