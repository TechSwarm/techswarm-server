from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import tsserver


engine = None
Base = None


def connect_db():
    global engine, Base
    if engine is not None:
        return

    # See: http://docs.sqlalchemy.org/en/latest/core/engines.html
    # URL Format: dialect+driver://username:password@host:port/database
    # OR SQLite: sqlite://<nohostname>/<path>
    engine = create_engine(tsserver.app.config['DATABASE'],
                           convert_unicode=True)
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
