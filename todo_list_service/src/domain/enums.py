from enum import Enum

class Environment(str, Enum):
    DEV = "dev"
    TEST = "test"
    PROD = "prod"
    
class DBStack(str, Enum):
    POSTGRESQL = "postgresql"
    MONGO_DB = "mongo_db"

class Status(str, Enum):
    pending = "pending"
    in_progress = "in-progress"
    completed = "completed"
    give_up = "give-up"
    
class Priority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"