
from dataclasses import dataclass

# Contains all runtime data that needs to be transfered between stages
@dataclass
class Data:
    
    # Data entries
    matrix : list[list] = None