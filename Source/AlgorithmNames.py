from enum import Enum


class AlgorithmNames(Enum):

    HUNGARIAN = 0
    GREEDY = 1
    THRIFTY = 2
    GREEDY_THRIFTY = 3
    THRIFTY_GREEDY = 4
    BkJ = 5
    CTG = 6
    MINIMAL = 7
    RANDOM = 8
    FAST_ROTTING_FIRST = 9  # типа те кто быстрее всего гниют тех выбираем первыми
