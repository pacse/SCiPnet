"""
Core SQLAlchemy utilities

Contains
--------
engine : Engine
    Global SQLAlchemy engine instance
db_session : ContextManager
    Context manager for automatic session management


Notes
-----
- Made primarily by Github Copilot
"""

from .engine import engine
from .session import db_session

__all__ = ['engine', 'db_session']
