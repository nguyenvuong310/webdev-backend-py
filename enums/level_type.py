from enum import Enum

class LevelType(Enum):
    LEVEL1 = '>=8'
    LEVEL2 = '6 <= && < 8'
    LEVEL3 = '4 <= && < 6'
    LEVEL4 = '< 4'