"""
Base classes, functions, & mixins

Exports
-------
- Constants
    - WK_HASH_REGEX
    - VALID_TABLES
    - VALID_MODELS
- Validation helpers
    - validate_table
    - validate_model
- Column helpers
    - col_int_pk
    - col_int_fk
    - col_str
    - wk_hash
    - rel
- Mixins
    - HelperTableMixin
    - MainTableMixin
- ORM base class
    - Base
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped

from datetime import datetime, timezone as tz
from typing import Literal, Any



# === Constants ===

WK_HASH_REGEX = r'scrypt:32768:8:1\$[A-Za-z0-9]{16}\$[A-Za-z0-9]{128}'
"""werkzeug hash regex for validation"""

VALID_TABLES = {
                'users',
                'scps',
                'mtfs',
                'sites',
                'audit_log',

                'clearance_lvls',
                'containment_classes',
                'secondary_classes',
                'disruption_classes',
                'risk_classes',
                'titles',
               }
"""
Valid table names for SQL queries

- Main Tables
    - users
    - scps
    - mtfs
    - sites
    - audit_log

- Helper Tables
    - clearance_lvls
    - containment_classes
    - secondary_classes
    - disruption_classes
    - risk_classes
    - titles
"""

VALID_MODELS = {
                'User',
                'SCP',
                'MTF',
                'Site',
                'AuditLog',

                'ClearanceLvl',
                'ContainmentClass',
                'SecondaryClass',
                'DisruptionClass',
                'RiskClass',
                'Title',
               }
"""
Valid model names for SQLAlchemy

- Main Models
    - User
    - SCP
    - MTF
    - Site
    - AuditLog

- Helper Models
    - ClearanceLvl
    - ContainmentClass
    - SecondaryClass
    - DisruptionClass
    - RiskClass
    - Title
"""



# === Validation helpers ===

def _check_name_against_list(
                             name: str,
                             valid_names: set[str]
                            ) -> bool:
    """
    Checks `name` is in `valid_names`

    Parameters
    ----------
    name : str
        Name to check
    valid_names : set[str]
        Set of valid names
    """

    if not isinstance(name, str) or name not in valid_names:
        return False

    return True

def validate_table(t_name: str) -> bool:
    """
    Checks `t_name` against `VALID_TABLES`

    Parameters
    ----------
    t_name : str
        Table name to validate

    Returns
    -------
    bool
        - True if valid
        - False if `t_name` is not a string
        - False if `t_name` is not in `VALID_TABLES`
    """

    return _check_name_against_list(t_name, VALID_TABLES)

def validate_model(m_name: str) -> bool:
    """
    Checks `m_name` against `VALID_MODELS`

    Parameters
    ----------
    m_name : str
        Model name to validate

    Returns
    -------
    bool
        - True if valid
        - False if `m_name` is not a string
        - False if `m_name` is not in `VALID_MODELS`
    """

    return _check_name_against_list(m_name, VALID_MODELS)



# === Column helpers ===

def col_int_pk() -> Column[int]:
    """
    Returns a primary key integer column with autoincrement.
    """
    return Column(Integer, primary_key=True, autoincrement=True)

def col_int_fk(
               ref: str,
               nullable = False,
               index = True
              ) -> Column[int]:
    """
    Returns a foreign key integer column.

    Parameters
    ----------
    ref : str
        Reference table and column in format `<table_name>.<column_name>`
    nullable : bool, default=False
        Whether the column is nullable
    indexed : bool, default=False
        Whether to index the column
    """
    return Column(Integer, ForeignKey(ref), nullable=nullable, index=index)


def col_str(
            length: int,
            nullable: bool = True,
            index: bool = True
           ) -> Column[str]:
    """
    Returns a string column.

    Parameters
    ----------
    length : int
        Maximum length of the string
    nullable : bool, default=True
        Whether the column is nullable
    index : bool, default=True
        Whether to index the column
    """
    return Column(String(length), nullable=nullable, index=index)

def wk_hash(
            nullable: bool,
            index: bool = True
           ) -> Column[str]:
    """
    Returns a string column for storing a werkzeug password hash.

    Parameters
    ----------
    nullable : bool
        Whether the column is nullable
    index : bool, default=True
        Whether to index the column
    """
    return col_str(162, nullable, index) # 162 is max length of werkzeug hash


def col_datetime(
                 onupdate: bool = False,
                 nullable: bool = False,
                 index: bool = True
                ) -> Column[datetime]:
    """
    Returns a DateTime column defaulting to current UTC time.

    Parameters
    ----------
    onupdate : bool, default=False
        Whether to have the column update on row update
    nullable : bool, default=False
        Whether the column is nullable
    index : bool, default=True
        Whether to index the column
    """
    return Column(
                  DateTime,
                  default=datetime.now(tz.utc),
                  onupdate=datetime.now(tz.utc) if onupdate else None,
                  nullable=nullable,
                  index=index
                 )


def rel(
        back_pop: str,
        keys: list[Column[Any]] | str | None = None,
        *, # force keyword args
        to: str | None = None,
       ) -> Mapped[Any]:
    """
    Returns a relationship to another table.

    Parameters
    ----------
    back_pop : str
        Back-populates target model name (e.g. 'users', 'scps', etc)
    keys : list[Column[Any]] or str or None, default=None
        Foreign key column(s) to use for relationship
    to : str or None, default=None
        Target model name (eg. 'User', 'SCP', etc)

    Returns
    -------
    Mapped[Any]
        Relationship mapping
    """
    return relationship(to, back_populates=back_pop, foreign_keys=keys)



# === Mixins ===

class MainTableMixin:
    """
    Mixin for main tables

    Columns
    -------
    created_at : datetime
        Indexed created_at timestamp column
    updated_at : datetime
        Indexed updated_at timestamp column
    """
    created_at = col_datetime()
    updated_at = col_datetime(True)


class HelperTableMixin:
    """
    Mixin for helper tables

    Columns
    -------
    name : str
        Indexed name column (50 chars)

    created_at : datetime
        Indexed created_at timestamp column
    updated_at : datetime
        Indexed updated_at timestamp column
    """
    name = col_str(50, False, True)

    created_at = col_datetime(      index = False)
    updated_at = col_datetime(True, index = False)



# === ORM table base class ===

class Base(DeclarativeBase):
    """
    Base class for SQLAlchemy ORM models.

    Columns
    -------
    id : int
        Primary key integer column

    Methods
    -------
    __repr__()
        String representation of the model
        Formatted as: '<ClassName(attr1=value1, attr2=value2, ...)>'
    """
    id = col_int_pk()

    def __repr__(self):
        cols = self.__mapper__.columns
        attrs = [
                 f'{col.key}={getattr(self, col.key)!r}'
                 for col in cols
                ]

        return f'<{self.__class__.__name__}({", ".join(attrs)})>'



# === Exports ===
__all__ = [
           # constants
           'WK_HASH_REGEX',
           'VALID_TABLES',
           'VALID_MODELS',

           # validation helpers
           'validate_table',
           'validate_model',

           # Col helpers
           'col_int_pk',
           'col_int_fk',
           'col_str',
           'wk_hash',
           'col_datetime',
           'rel',

           # Mixins
           'HelperTableMixin',
           'MainTableMixin',

           # Base
           'Base',
          ]
