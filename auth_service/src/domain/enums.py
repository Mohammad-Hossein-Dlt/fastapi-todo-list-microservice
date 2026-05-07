from enum import Enum

class Environment(str, Enum):
    DEV = "dev"
    TEST = "test"
    PROD = "prod"
    
class DBStack(str, Enum):
    POSTGRESQL = "postgresql"
    MONGO_DB = "mongo_db"
    
class Role(str, Enum):
    ADMIN = "admin"    
    USER = "user"    