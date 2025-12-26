"""
SQL query helpers and common queries

Contains
--------
- get_field
- get_next_id
- log_event
"""

from typing import Any, Generator, TypeVar
from ipaddress import ip_address
from contextlib import contextmanager

from sqlalchemy import select, func
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm import Session

from .core import db_session
from .schema import MainModels as ORMModels, ORMBase, validate_table
from ..general.exceptions import TableNotFoundError, RecordNotFoundError, \
                        DatabaseError, DatabaseSessionError, field_error
from ..general.validation import validate_field, validate_str, \
                                 validate_int, validate_model_field



# === Types ===

T = TypeVar('T', bound=ORMBase) # Generic type for SQLAlchemy models



# === Helpers ===

def _get_table_name(model_class: type[ORMBase]) -> str:
    """
    Returns a type[Base]'s tablename
    """
    return model_class.__tablename__


@contextmanager
def db_session_manager(
                       model_class: type[ORMBase],
                       fields: list[str] = []
                      ) -> Generator[
                                     tuple[str, Session, set[Any]],
                                     None, None
                                    ]:
    """
    Extends db_session to have basic validation

    Parameters
    ----------
    model_class : type[Base]
        The model class (table) to validate
    fields : list[str] = []
        list of field names to validate and return as model attributes

    Yields
    ------
    tuple[str, Session, set[Any]]
        - Table name
        - SQLAlchemy session
        - Set of model attributes (columns) corresponding to `fields`


    Raises
    ------
    TableNotFoundError
        If `model_class` does not correspond to a valid table
    TypeError
        If any field in `fields` is not a str
    ValueError
        If any field in `fields` is empty or whitespace-only
    ColumnNotFoundError
        If any field in `fields` does not exist in the table
    DatabaseSessionError
        If there was an error creating the session
    """
    t_name = _get_table_name(model_class)

    if not validate_table(t_name):
        raise TableNotFoundError(t_name)

    attrs = []
    for field in fields:
        validate_model_field(model_class, field)
        attrs.append(getattr(model_class, field))

    # ensure unique fields
    if len(attrs) != len(set(attrs)):
        raise field_error(
            'fields', fields,
            'list of unique field names'
        )

    with db_session() as session:
        yield t_name, session, set(attrs)



# === Main funcs ===

def get_field(
              model_class: type[ORMBase],
              return_field: str,
              filter_field: str,
              filter_value: Any,
             ) -> Any:
    """
    A generic field lookup function.

    SELECT `return_field` FROM `model_class` WHERE `filter_field` = `filter_value`

    Parameters
    ----------
    model_class : type[Base]
        The model class (table) to query
    return_field : str
        The field to return
    filter_field : str
        The field to filter on
    filter_value : Any
        The value to filter by

    Returns
    -------
    Any
        The value of the field

    Raises
    ------
    TableNotFoundError
        If `model_class` does not correspond to a valid table
    TypeError
        If `return_field` is not a str
    ColumnNotFoundError
        - If `return_field` does not exist in the table
        - If any filter field does not exist in the table
    RecordNotFoundError
        If no record matches the lookup criteria

    Notes
    -----
    **Never pass raw user input**
    """

    with db_session_manager(
        model_class,
        [return_field, filter_field]
    ) as (
        t_name,
        session,
        (return_col, filter_col)
    ):
        result = session.scalar(
            select(return_col).filter(
                filter_col == filter_value
            )
        )

    # ensure we got something & return it
    if result:
        return result
    raise RecordNotFoundError(filter_field, filter_value, t_name)


def get_model(
              model_class: type[T],
              model_id: int,
             ) -> T:
    """
    Gets a full model (row) by ID

    Parameters
    ----------
    model_class : type[Base]
        The model class (table) to query
    model_id : int
        The ID of the model (row) to get

    Returns
    -------
    Base
        The model (row)

    Raises
    ------
    TableNotFoundError
        If `model_class` does not correspond to a valid table
    RecordNotFoundError
        If no record with `model.id = model_id` exists
    """

    with db_session_manager(model_class) as (t_name, session, _):
        result = session.get(model_class, model_id)

    if result:
        return result
    raise RecordNotFoundError('id', model_id, t_name)


def get_next_id(model_class: type[ORMBase]) -> int:
    """
    Returns the next id in a table:
    COALESCE(MAX(id), 0) + 1

    Parameters
    ----------
    model_class : type[Base]
        The model class (table) to get the next ID for

    Returns
    -------
    int
        The next ID

    Raises
    ------
    TableNotFoundError
        If `model_class` does not correspond to a valid table
    DatabaseError
        If there was an error executing the query
    """

    with db_session_manager(model_class) as (t_name, session, _):
            result = session.scalar(
                select(
                    func.coalesce(
                        func.max(model_class.id), 0
                    ) + 1
            ))

    # check result to make type checker happy
    if result:
        return result
    raise DatabaseError(
        f'Failed to get next ID for table {t_name}: '
        'COALESCE(MAX(id), 0) + 1 returned None'
    )


def log_event(
              user_id: int,
              user_ip: str,
              action: str,
              details: str,
              status: bool = True
             ) -> None:
    """
    Logs an event in the audit log
    (eg. account creation, login, file access, file edit, etc.)

    Parameters
    ----------
    user_id : int
        The ID of the user performing the action
    user_ip : str
        The IP address of the user performing the action
    action : str
        A short description of the action
    details : str
        Additional details about the action
    status : bool, default=True
        The status of the action (successful or not)

    Raises
    ------
    TypeError
        If any parameter is of the wrong type
    FieldError
        - If `user_id` is not a positive int
        - If any str parameter is an empty or whitespace-only string
        - If `user_ip` is not a valid IP address
    """

    # validate inputs
    validate_int('user_id', user_id)

    for name, value in [
        ('user_ip', user_ip),
        ('action', action),
        ('details', details)
    ]:
        validate_str(name, value)

    validate_field('status', status, bool)

    try:
        ip_address(user_ip)
    except ValueError as e:
        raise field_error(
            'user_ip', user_ip,
            'valid IP address (IPv4 or IPv6)'
        ) from e

    # actual logic
    try:
        row = ORMModels.AuditLog(
            user_id=user_id,
            user_ip=user_ip,
            action=action,
            details=details,
            status=status
        )

        with db_session() as session:
            session.add(row)

    except IntegrityError as e:
        raise DatabaseError(
            f'Audit log constraint violation: {e}'
        ) from e
    except SQLAlchemyError as e:
        raise DatabaseSessionError(
            f'Failed to log event: {e}'
        ) from e



# === Exports ===
__all__ = ['get_field', 'get_next_id', 'log_event']
