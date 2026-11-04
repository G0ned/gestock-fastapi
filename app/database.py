from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Carga las variables del archivo .env (en la raíz del proyecto) si existe.
# No sobrescribe las variables que ya estén definidas (p. ej. las de Docker).
load_dotenv()

#<conexion>://<username>:<password>@<host>:<port>/<database>

connection = os.getenv("DB_CONNECTION")
username = os.getenv("DB_USERNAME")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
database = os.getenv("DB_DATABASE")

_missing = [name for name, value in {
    "DB_CONNECTION": connection, "DB_USERNAME": username, "DB_PASSWORD": password,
    "DB_HOST": host, "DB_PORT": port, "DB_DATABASE": database,
}.items() if not value]
if _missing:
    raise RuntimeError(f"Faltan variables de entorno: {', '.join(_missing)}. Revisa el archivo .env")

db_url = f"{connection}{username}:{password}@{host}:{port}/{database}"

engine = create_engine(db_url)
session = sessionmaker(autocommit=False, bind=engine)

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()