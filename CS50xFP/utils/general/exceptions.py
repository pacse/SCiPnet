"""
All custom exceptions

Contains
--------
- SQLite DB related exceptions
    - DatabaseError

    - TableNotFoundError
    - ColumnNotFoundError
    - RecordNotFoundError

    - DatabaseNotFoundError
    - DatabaseConnectionError
    - DatabaseSessionError

- General exceptions
    - FieldError
    - ArgumentError
"""

from typing import Any
from humanize import naturalsize as hsize

# maybe useful later ¯\_(ツ)_/¯
'''
def format_error_str(
                     operation: str,
                     table_name: str,
                     details: str
                    ) -> str:
    """
    Helper to format error strings consistently
    """
    #f'Failed to get next ID for {table_name}:\n{e}'
    #
    return f'Failed to {operation} from table {table_name!r}:\n{details}'
'''



# === SQLite Database related exceptions ===

class DatabaseError(Exception):
    """
    Base exception for SQLite Database related errors
    """
    pass


class TableNotFoundError(DatabaseError):
    """
    Raised when a specified table does not exist

    Parameters
    ----------
    table_name : str
        The name of the table that does not exist

    Error Message
    -------------
        >>> f'Table {table_name!r} does not exist.'
    """
    def __init__(self, table_name: str):
        super().__init__(f'Table {table_name!r} does not exist.')

class ColumnNotFoundError(DatabaseError):
    """
    Raised when a specified column does not exist

    Parameters
    ----------
    column_name : str
        The name of the column that does not exist
    table_name : str
        The name of the table being queried

    Error Message
    -------------
        >>> f'Column {column_name!r} does not exist in table {table_name!r}.'
    """
    def __init__(self, column_name: str, table_name: str):
        super().__init__(
            f'Column {column_name!r} '
            f'does not exist in table {table_name!r}.'
        )

class RecordNotFoundError(DatabaseError):
    """
    Raised when a specified record (row) does not exist in a table

    Parameters
    ----------
    lookup_field : str
        The field used to look up the record
    lookup_value : Any
        The value of the lookup field
    table_name : str
        The name of the table being queried

    Error Message
    -------------
        >>> f'Record with {lookup_field!r} = {lookup_value!r} does not exist in table {table_name!r}.'
    """
    def __init__(self,
                 lookup_field: str,
                 lookup_value: Any,
                 table_name: str,
                ):
        super().__init__(
            f'Record with {lookup_field!r} = {lookup_value!r}'
            f' does not exist in table {table_name!r}.'
        )


class DatabaseNotFoundError(DatabaseError):
    """
    Raised when the SQLite database file is not found

    Error Message
    -------------
        >>> 'Database file not found.'
    """
    def __init__(self):
        super().__init__('Database file not found.')

class DatabaseConnectionError(DatabaseError):
    """
    Raised when a database connection fails
    """
    pass

class DatabaseSessionError(DatabaseError):
    """
    Raised when a session operation fails
    """
    pass



# === Socket related exceptions ===

class MaxSizeLimitError(Exception):
    """
    Raised when the message/data size exceeds maximum allowed size

    Parameters
    ----------
    data_size : int
        The size of the data/message in bytes
    max_size : int
        The maximum allowed size in bytes
    use_data : bool
        Whether to use 'Data' or 'Message' in the error message

    Error Message
    -------------
        >>> f'{"Data" if use_data else "Message"}'
        f' size ({hsize(data_size)}) exceeds'
        f' maximum size ({hsize(max_size)})'
    """
    def __init__(self,
                 data_size: int,
                 max_size: int,
                 use_data: bool = True
                ):
        label = 'Data' if use_data else 'Message'
        super().__init__(
            f'{label} size ({hsize(data_size)}) exceeds'
            f' maximum size ({hsize(max_size)})'
        )



# === General exceptions ===

def _gen_error_str(
                   invalid: str,
                   value: Any,
                   expected: str
                  ) -> str:
    """
    Helper to format error strings consistently

    Returns
    -------
    str
        f'Invalid {invalid}: {value!r} (expected {expected})'
    """
    return f'Invalid {invalid}: {value!r} (expected {expected})'


def field_error(
                field: str,
                field_val: Any,
                expected: str
               ) -> ValueError:
    """
    A formatted ValueError

    Parameters
    ----------
    field : str
        The name of the field with the error
    field_val : Any
        The invalid value of the field
    expected : str
        Description of the expected value/type

    Error Message
    -------------
        >>> f'Invalid {field}: {field_val!r} (expected {expected})'
    """
    return ValueError(_gen_error_str(
                        field, field_val, expected
                      ))

def arg_error(
              arg_name: str,
              arg_val: Any,
              expected_type: Any,
             ) -> TypeError:
    """
    A formatted TypeError

    Parameters
    ----------
    arg_name : str
        The name of the argument
    arg_val : Any
        The invalid argument value
    expected_type : Any
        The expected type


    Error Message
    -------------
        >>> f'''Invalid {arg_name} type: {type(arg_val).__name__}
            (expected {expected_type.__name__})'''
    """
    return TypeError(_gen_error_str(
                        f'type of {arg_name}',
                        type(arg_val).__name__,
                        f'{expected_type.__name__!r}'
                      ))


__all__ = [
           # SQLite related exceptions
           'DatabaseError',
           'TableNotFoundError',
           'ColumnNotFoundError',
           'RecordNotFoundError',
           'DatabaseNotFoundError',
           'DatabaseConnectionError',
           'DatabaseSessionError',

           # Socket related exceptions
           'MaxSizeLimitError',

           # General exceptions
           'field_error',
           'arg_error',
]
