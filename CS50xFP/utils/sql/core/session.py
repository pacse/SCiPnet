"""
Session management for database interactions

Contains
--------
- Session_Factory
- Session
- db_session

Notes
-----
- Made primarily by Github Copilot
"""

from .engine import engine
from ...general.exceptions import DatabaseSessionError

from sqlalchemy.orm import sessionmaker, scoped_session, \
                           Session as SessionType
from contextlib import contextmanager
from typing import Generator

# create a factory to generate new sessions
_session_factory = sessionmaker(bind=engine)
# ensures each thread gets its own session
Session = scoped_session(_session_factory)


@contextmanager  # allows func to use `with`
def db_session() -> Generator[SessionType, None, None]:
    """
    Handles creation, usage, and cleanup of a db session

    Yields
    ------
    sqlalchemy.orm.Session
        A database session

    Raises
    ------
    DatabaseSessionError
        If an error occurs during session operations

    Example
    -------
    >>> with db_session() as session:
    ...    session.add(some_object)
    ...    session.query(SomeModel)
    """

    session = None
    try:
        session = Session()  # create a new session
        yield session        # give it to the caller
        session.commit()     # commit what they did

    except Exception as e:
        if session:  # only rollback if session exists
            session.rollback()

        raise DatabaseSessionError(
            f'Database session operation failed: {e}'
        ) from e

    finally:
        if session:  # always close session if it exists
            session.close()



# === Exports ===
__all__ = ['db_session']
