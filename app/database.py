from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

#<conexion>://<username>:<password>@<host>:<port>/<database>

connection = os.getenv("DB_CONNECTION")
username = os.getenv("DB_USERNAME")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
database = os.getenv("DB_DATABASE")

db_url = f"{connection}{username}:{password}@{host}:{port}/{database}"

engine = create_engine(db_url)
session = sessionmaker(autocommit=False, bind=engine)

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()