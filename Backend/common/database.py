import pymysql
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
import os

DATABASE_URL = os.environ.get("DATABASE_URL")


pymysql.install_as_MySQLdb()

engine = create_engine(
    DATABASE_URL,
    poolclass=NullPool,
)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base: DeclarativeMeta = declarative_base()


def get_db():
    session = Session()
    try:
        yield session
    finally:
        print("db close")
        session.close()
