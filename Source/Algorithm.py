from abc import ABC, abstractmethod
from Data import Data


class Algorithm(ABC):
    
    def __init__(self):
        pass
    
    # Basic method to be overriden,
    # Does not change input data,
    # Returns updated data
    @staticmethod
    @abstractmethod
    def run(input_data : Data) -> Data:
        pass