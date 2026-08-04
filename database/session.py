from sqlmodel import Session

from database.connection import engine


def get_session():
    return Session(engine)