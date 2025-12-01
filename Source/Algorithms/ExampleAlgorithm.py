from Algorithm import Algorithm
from Data import Data, Statistics
from copy import copy


class ExampleAlgorithm(Algorithm):
    
    def __init__(self):
        super().__init__()
       
    # Basic method to be overriden,
    # Changes input data,
    # Returns nothing
    @staticmethod
    def run(input_data : Data) -> None:
        None
        # Modifies data somehow
        # new_data.matrix = list()
