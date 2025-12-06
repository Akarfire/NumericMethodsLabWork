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
    greedy_thrifty_stage : int = 5  # in [2, floor(n / 2)] (ограничений в методичке не было, взял по аналогии с thrifty_greedy_stage)
    thrifty_greedy_stage : int = 5  # in [2, floor(n / 2)]

    bkj_stage : int = 5  # in [1, n] (ограничений в методичке не было, но можно взять и [2, floor(n / 2)] по аналогии с остальными)
    bkj_rank : int = 2  # в методичке in [1, n - bkj_stage + 1]; actually in [1, n - bkj_stage + 2]

    ctg_stage : int = 5  # in [2, floor(n / 2)]

    # Data entries
    matrix : list[list] = field(default_factory=list)
    
    statistics : Statistics = field(default_factory=Statistics)