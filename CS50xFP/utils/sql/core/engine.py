"""
Database engine creation and configuration

Contains
--------
- create_db_engine
- engine

Notes
-----
- engine is a global `Engine` instance created at import
- Made primarily by Github Copilot
"""

from sqlalchemy import Engine, create_engine
from ...general.sql_config import Config, DEEPWELL_DIR, DB_URL
from ...general.exceptions import DatabaseConnectionError


def create_db_engine() -> Engine:
    """
    Creates a new SQLAlchemy database engine with
    settings from config.py for pool & SQLite

    Returns
    -------
    sqlalchemy.engine.Engine
        The created database engine
    """

    # validate DB path
    if not DEEPWELL_DIR.exists():
        raise DatabaseConnectionError(
            f'Database directory does not exist: {DEEPWELL_DIR}'
        )

    try:
        return create_engine(
                             DB_URL,          # path to SQLite database
                             **Config.POOL,   # unpack pool config settings
                             **Config.SQLITE  # unpack SQLite config settings
                            )

    except Exception as e:
        raise DatabaseConnectionError(
            f'Failed to create database engine: {e}'
        ) from e


# create a global engine instance, crashes import if init fails
engine = create_db_engine()

# === Exports ===
__all__ = ['engine']
