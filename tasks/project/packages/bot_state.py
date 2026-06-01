from enum import Enum

class BotState(Enum):
    convoying = 0
    waiting = 1
    turning = 2
    finishing = 3