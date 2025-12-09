from Data import Data, Statistics
from AlgorithmNames import AlgorithmNames

from dataclasses import dataclass, field

@dataclass
class Results:
    
    # Some results that are going to be sent back to the UI for display
    
    # Final results statistics should be in a sorted order
    statistics_list : list[list[str, float]] = field(default_factory=list)
    statistics : dict[str : list[float]] = field(default_factory=dict)
    
    best_strategy : str = "GREEDY"
    worst_strategy : str = "GREEDY"

