from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import dotenv_values

config_env = {
    **dotenv_values(".env"), 
    **os.environ,  
}


DB_HOST=config_env["DB_HOST"]
DB_USER=config_env["DB_USER"]
DB_PASSWORD=config_env["DB_PASSWORD"]
DB_NAME=config_env["DB_NAME"]
DB_PORT=config_env["DB_PORT"]



URL = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
print(URL)
engine = create_engine(URL)
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()