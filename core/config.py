from sqlalchemy import create_engine, engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy_utils import has_index
from core.settings import get_db_credentials



PROJECT_NAME = "Exchange-Nija"
VERSION = "1.0.0"
API_PREFIX = "/api"




def get_engine(user, password,host,port,db):
    url=f"postgresql://{user}:{password}@{host}:{port}/{db}"
    if not database_exists(url):
        create_database(url)
    engine =create_engine(url, pool_size=50, echo=False)
    return engine

def get_url():
    settings=get_db_credentials()
    return f"postgresql://{settings['POSTGRES_USER']}:{settings['POSTGRES_PASSWORD']}@{settings['POSTGRES_SERVER']}:{settings['POSTGRES_PORT']}/{settings['POSTGRES_DB']}"



# settings=get_db_credentials()
# url=get_engine(settings['POSTGRES_USER'],settings['POSTGRES_PASSWORD'],settings['POSTGRES_SERVER'],settings['POSTGRES_PORT'],settings['POSTGRES_DB'])   
# print(url)

def get_engine_from_settings():
    settings=get_db_credentials()
    keys=['POSTGRES_USER','POSTGRES_PASSWORD','POSTGRES_SERVER','POSTGRES_PORT','POSTGRES_DB']
    if not all(key in keys for key in settings.keys()):
        raise Exception('Bad Config file')
    return get_engine(settings['POSTGRES_USER'],settings['POSTGRES_PASSWORD'],settings['POSTGRES_SERVER'],settings['POSTGRES_PORT'],settings['POSTGRES_DB'])

def get_sessions():
    engine = get_engine_from_settings()
    sessions = sessionmaker(autocommit=False, autoflush=False,bind=engine)
    return sessions


def get_db():
    sessions = get_sessions()
    db = sessions()
    try:
        yield db
    except:
        db.rollback()
        raise
    finally:
        db.close()

