from dataclasses import dataclass, field
from AlgorithmNames import AlgorithmNames

@dataclass
class Statistics:
    
    sugarity_data_per_algorithm : dict[AlgorithmNames, list[float]] = field(default_factory=dict)
    

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
    matrix : list[list] = field(default_factory=list)
    
    statistics : Statistics = Statistics()