from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import tsserver


# Values to these globals are set in connect_db(), since database config
# is read from app config (which can be changed after importing this file,
# but before actually doing anything with the database)
engine = None
Base = None


def connect_db():
    global engine, Base
    if engine is not None:
        return

    engine = create_engine(tsserver.app.config['DATABASE_URL'],
                           **tsserver.app.config['DATABASE_SETTINGS'])
    db_session = scoped_session(sessionmaker(autocommit=False,
                                             autoflush=False,
                                             bind=engine))
    Base = declarative_base()
    Base.query = db_session.query_property()


def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import models

    Base.metadata.create_all(bind=engine)
