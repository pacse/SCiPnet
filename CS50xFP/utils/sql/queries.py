"""
SQL query helpers and common queries

Contains
--------
- get_field
- get_next_id
- log_event
"""

from typing import TypeAlias, Any

from sqlalchemy import select, func
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from ipaddress import ip_address

from .core import db_session
from .schema import MainModels, Base, validate_table
from ..general.exceptions import TableNotFoundError, RecordNotFoundError, \
                        ColumnNotFoundError, DatabaseError, \
                        DatabaseSessionError, FieldError, ArgumentError
from ..general.validation import _validate_field, _validate_str, _validate_int


# === Types ===

ModelClass: TypeAlias = type[Base]



# === Helpers ===

def _get_table_name(model_class: ModelClass) -> str:
    """
    Returns a ModelClass's tablename
    """
    return model_class.__tablename__



# === Main funcs ===

def get_field(
              model_class: ModelClass,
              return_field: str,
              filter_field: str,
              filter_value: Any,
             ) -> Any:
    """
    A generic field lookup function.

    SELECT `return_field` FROM `model_class` WHERE `filter_field` = `filter_value`

    Parameters
    ----------
    model_class : ModelClass
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

    t_name = _get_table_name(model_class)

    # validation
    if not validate_table(t_name):
        raise TableNotFoundError(t_name)

    if not isinstance(return_field, str):
        raise ArgumentError('return_field', return_field, 'str')
    if not isinstance(filter_field, str):
        raise ArgumentError('filter_field', filter_field, 'str')

    if not hasattr(model_class, filter_field):
        raise ColumnNotFoundError(t_name, filter_field)
    if not hasattr(model_class, return_field):
        raise ColumnNotFoundError(t_name, return_field)


    # build & execute query
    return_col = getattr(model_class, return_field)
    filter_col = getattr(model_class, filter_field)

    with db_session() as session:
            result = session.scalar(
                select(return_col).filter(filter_col == filter_value)
            )

    # ensure we got something & return it
    if result is None:
        raise RecordNotFoundError(
                                  filter_field,
                                  filter_value,
                                  t_name
                                 )
    return result


def get_next_id(model_class: ModelClass) -> int:
    """
    Returns the next id in a table:
    COALESCE(MAX(id), 0) + 1

    Parameters
    ----------
    model_class : ModelClass
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

    t_name = _get_table_name(model_class)

    # validation
    if not validate_table(t_name):
        raise TableNotFoundError(t_name)

    # exec query
    with db_session() as session:
            result = session.scalar(select(
                func.coalesce(func.max(model_class.id), 0) + 1
            ))

    # check result to make type checker happy
    if result is None:
        raise DatabaseError(
            f'Failed to get next ID for table {t_name}: '
            'COALESCE(MAX(id), 0) + 1 returned None'
        )

    return result


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
    _validate_int('user_id', user_id)

    for name, value in [
        ('user_ip', user_ip),
        ('action', action),
        ('details', details)
    ]:
        _validate_str(name, value)

    _validate_field('status', status, bool)

    try:
        ip_address(user_ip)
    except ValueError as e:
        raise FieldError(
            'user_ip', user_ip,
            'valid IP address (IPv4 or IPv6)'
        ) from e

    # actual logic
    try:
        row = MainModels.AuditLog(
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
