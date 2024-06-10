from enum import Enum


class ResultStatus(Enum):
    SUCCESS = 1
    ERROR = 2


class SearchType(Enum):
    SUBSTRUCTURE = 1
    SUPERSTRUCTURE = 2
    EXACT = 3
    SIMILARITY = 4
    PERFECT = 5
    EXACT_FRAGMENT = 6
