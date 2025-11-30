from dataclasses import dataclass
from AlgorithmNames import AlgorithmNames

@dataclass
class Statistics:
    
    sugarity_data_per_algorithm : dict[AlgorithmNames, list[float]] = dict()
    

# Contains all runtime data that needs to be transfered between stages
@dataclass
class Data:
    
    n : int = 15
    m : float = 3000
    
    experiment_count : int = 100
    
    # Additional Algorithm Data
    greedy_thrifty_stages : int = 5
    thrifty_greedy_stages : int = 5
    
    bkj_rank : int = 2
    
    # Data entries
    matrix : list[list] = None
    
    statistics : Statistics = Statistics()