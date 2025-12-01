from Data import Data, Statistics
from AlgorithmNames import AlgorithmNames

from dataclasses import dataclass, asdict, field

@dataclass
class Results:
    
    # Some results that are going to be sent back to the UI for display
    statistics : Statistics = field(default_factory=Statistics)
    
    best_strategy : AlgorithmNames = AlgorithmNames.GREEDY
    worst_strategy : AlgorithmNames = AlgorithmNames.GREEDY
    
    # Converts results structure into a dict for sending
    def dict(self) -> dict:
        return {k: str(v) for k, v in asdict(self).items()}

