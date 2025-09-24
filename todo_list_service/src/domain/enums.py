from enum import Enum

class Status(str, Enum):
    pending = "pending"
    in_progress = "in-progress"
    completed = "completed"
    give_up = "give-up"
    
class Priority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"