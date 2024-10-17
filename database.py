from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask_security.models import sqla
import os

server = os.getenv('SERVER')
port = os.getenv('PORT')
username = os.getenv('USER')
password = os.getenv('PASSWORD')

engine = create_engine(f'mysql+mysqlconnector://{username}:{password}@{server}:{port}/pythonlogin')
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
# This creates the RolesUser table and is where
# you would pass in non-standard tables names.
sqla.FsModels.set_db_info(base_model=Base)


def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import models
    Base.metadata.create_all(bind=engine)