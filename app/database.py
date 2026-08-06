from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
#<conexion>://<username>:<password>@<host>:<port>/<database>
db_url = f"{os.getenv("DB_CONNECTION")}{os.getenv("DB_USERNAME")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}/{os.getenv("DB_DATABASE")}"
engine = create_engine(db_url)
session = sessionmaker(autocommit=False, bind=engine)

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()