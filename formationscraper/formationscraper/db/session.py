from sqlalchemy import create_engine, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from ..core.config import settings

load_dotenv()

Base = declarative_base()


def get_engine(url):
    return create_engine(url, echo=True, pool_pre_ping=True) 

def get_session(url):
    engine = get_engine(url)
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    return SessionLocal

def choice_bdd() :
    ### pour intégrer les settings du fichier config.py au lieu de os.get.env
    if settings.IS_POSTGRES==1:
        username = settings.DB_USERNAME
        password = settings.DB_PASSWORD
        hostname = settings.DB_HOSTNAME
        port = settings.DB_PORT
        database_name = settings.DB_NAME
        bdd_path = f"postgresql://{username}:{password}@{hostname}:{port}/{database_name}"
    else:
        bdd_path = settings.DATABASE_SQLITE
    return bdd_path

# Dépendance de session
def get_db():
    url = choice_bdd()
    SessionLocal = get_session(url)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_datetype():
    path = choice_bdd()
    engine = get_engine(path)

    if engine.dialect.name == 'sqlite':
        date_type = String
    elif engine.dialect.name == 'postgresql':
        date_type = Date
    else:
        raise ValueError(f"SGBD non pris en charge : {engine.dialect.name}")
    return date_type
