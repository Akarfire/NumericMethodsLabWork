from Data import Data, Statistics
from AlgorithmNames import AlgorithmNames

from dataclasses import dataclass, asdict

@dataclass
class Results:
    
    # Some results that are going to be sent back to the UI for display
    statistics : Statistics = None
    
    best_strategy : AlgorithmNames = AlgorithmNames.GREEDY
    worst_strategy : AlgorithmNames = AlgorithmNames.GREEDY
    
    # Converts results structure into a dict for sending
    def dict(self) -> dict:
        return {k: str(v) for k, v in asdict(self).items()}

