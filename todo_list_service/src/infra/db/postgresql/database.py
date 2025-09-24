from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import Session, sessionmaker
import psycopg2
from psycopg2 import sql
from .models._base import Base

def check_and_create_database(
    host: str,
    port: int,
    username: str,
    password: str,
    db_name: str,
) -> bool:
    try:
        connection = psycopg2.connect(
            dbname="postgres",
            user=username,
            password=password,
            host=host,
            port=port
        )
        connection.autocommit = True
        cursor = connection.cursor()

        cursor.execute(
            sql.SQL("SELECT 1 FROM pg_database WHERE datname = %s"),
            [db_name]
        )
        exists = cursor.fetchone()

        if exists:
            print(f"Database '{db_name}' already exists.")
        else:
            cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))
            print(f"Database '{db_name}' has been created.")

        if connection:
            cursor.close()
            connection.close()
        
        return True

    except psycopg2.Error as e:
        print("An error occurred:", e)
        
        return False

def init_sql_client(
    host: str,
    port: int,
    username: str,
    password: str,
    db_name: str,
) -> tuple[Session, Engine]:
    
    check = check_and_create_database(
        host=host,
        port=port,
        username=username,
        password=password,
        db_name=db_name,
    )
    
    if not check:
        return None, None
            
    BASE_URL = f"postgresql://{username}:{password}@{host}:{port}/{db_name}"

    engine = create_engine(BASE_URL)
    
    SessionLocal = sessionmaker(bind=engine)
    
    return SessionLocal(), engine

def create_tables(
    engine: Engine,
):
    Base.metadata.create_all(bind=engine)