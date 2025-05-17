import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Carga variables de entorno
load_dotenv()
raw_url = os.getenv("DATABASE_URL", "")
# Si la URL usa aiomysql la reemplazamos por pymysql para la parte síncrona
tmp = raw_url
if tmp.startswith("mysql+aiomysql"):
    sync_url = tmp.replace("mysql+aiomysql", "mysql+pymysql")
else:
    sync_url = tmp

engine = create_engine(sync_url, echo=True)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)