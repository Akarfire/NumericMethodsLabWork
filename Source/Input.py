from dataclasses import dataclass, field
from enum import Enum

class DegradationMode(Enum):
    UNIFORM = 1
    CONCENTRATED = 2

@dataclass
class Input:
    
    # General  
    n : int = 15
    m : float = 3000
    
    a_min : float = 0
    a_max : float = 1

    b_min : float = 0
    b_max : float = 1
    
    degradation_mode : DegradationMode = DegradationMode.UNIFORM
    concentrated_range_fraction : float = 0.25
    
    experiment_count : int = 100
    
    use_individual_ranges : bool = False
    individual_a_ranges : list[list[float, float]] = None
    individual_b_ranges : list[list[float, float]] = None
    
    # Additional Algorithm Data
    greedy_thrifty_stages : int = 5
    thrifty_greedy_stages : int = 5
    
    bkj_rank : int = 2
    
    # Non-organics
    use_non_organics : bool = False
    
    k_min : float = 5
    k_max : float = 7
    
    na_min : float = 0.21
    na_max : float = 0.82
    
    n_min : float = 1.5
    n_max : float = 2.8
    
    reduce_min : float = 0
    reduce_max : float = 1
    
    # Ripening
    use_ripening : bool = False
    
    ripening_stages : int = 5
    
    ripening_min : float = 1
    ripening_max : float = 1.15
    