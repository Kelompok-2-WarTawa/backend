import os
from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker
import zope.sqlalchemy


def get_session_factory(settings):
    engine = engine_from_config(settings, 'sqlalchemy.')
    return sessionmaker(bind=engine)


def get_tm_session(session_factory, transaction_manager):
    dbsession = session_factory()
    zope.sqlalchemy.register(
        dbsession, transaction_manager=transaction_manager)
    return dbsession
