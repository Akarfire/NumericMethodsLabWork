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
    
    a_min : float = 0.12
    a_max : float = 0.22

    b_min : float = 0.85
    b_max : float = 1
    
    degradation_mode : DegradationMode = DegradationMode.UNIFORM
    concentrated_range_fraction : float = 0.25
    
    experiment_count : int = 100
    
    use_individual_ranges : bool = False
    individual_a_ranges : list[list[float, float]] = field(default_factory=list)
    individual_b_ranges : list[list[float, float]] = field(default_factory=list)
    
    # Additional Algorithm Data
    greedy_thrifty_stage : int = 5  # in [2, floor(n / 2)] (ограничений в методичке не было, взял по аналогии с thrifty_greedy_stage)
    thrifty_greedy_stage : int = 5  # in [2, floor(n / 2)]

    bkj_stage : int = 5  # in [1, n] (ограничений в методичке не было, но можно взять и [2, floor(n / 2)] по аналогии с остальными)
    bkj_rank : int = 2  # в методичке in [1, n - bkj_stage + 1]; actually in [1, n - bkj_stage + 2]

    ctg_stage : int = 5  # in [2, floor(n / 2)]

    # Non-organics
    use_non_organics : bool = False
    
    k_min : float = 4.8
    k_max : float = 7.05
    
    na_min : float = 0.21
    na_max : float = 0.82
    
    n_min : float = 1.58
    n_max : float = 2.8
    
    reduce_min : float = 0.62
    reduce_max : float = 0.64
    
    # Ripening
    use_ripening : bool = False
    
    ripening_stages : int = 5
    
    ripening_min : float = 1
    ripening_max : float = 1.15
    