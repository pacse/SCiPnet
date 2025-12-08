"""
All custom exceptions for SQLite Database related errors
"""
from typing import Any

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

class DatabaseError(Exception):
    """
    Base exception for SQLite Database related errors
    """
    pass


class TableNotFoundError(DatabaseError):
    """
    Raised when a specified table does not exist
    """
    def __init__(self, table_name: str):
        super().__init__(f'Table {table_name!r} does not exist.')

class ColumnNotFoundError(DatabaseError):
    """
    Raised when a specified column does not exist
    """
    def __init__(self, column_name: str, table_name: str):
        super().__init__((
            f'Column {column_name!r} '
            f'does not exist in table {table_name!r}.'))

class RecordNotFoundError(DatabaseError):
    """
    Raised when a specified record (row) does not exist in a table
    """
    def __init__(self, table_name: str,
                 lookup_field: str,
                 lookup_value: str | int
                ):
        super().__init__((
            f'Record with {lookup_field!r} = {lookup_value!r}'
            f' does not exist in table {table_name!r}.'))


class DatabaseNotFoundError(DatabaseError):
    """
    Raised when the SQLite database file is not found
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


def FieldError(field: str,
               field_val: Any,
               expected: str
              ) -> ValueError:
    """
    A formatted ValueError:
    `Invalid {field}: {field_val!r} (expected {expected})`
    """
    return ValueError((f'Invalid {field}: {field_val!r}'
                       f' (expected {expected})'))

def ArgumentError(arg_val: Any,
                  expected_type_name: str,
                  arg_name: str = 'info',
                 ) -> TypeError:
    """
    A formatted TypeError:
    `Invalid {arg_name} type: {type(arg_val)} (expected {expected_type_name})`
    """
    return TypeError((f'Invalid {arg_name} type: {type(arg_val)}'
                       f' (expected {expected_type_name})'))
