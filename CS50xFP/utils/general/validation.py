"""
Useful validation functions

Contains
--------

"""

import socket
from typing import Any, get_type_hints
from enum import Enum
from re import fullmatch
from typing import TypeVar

from .exceptions import arg_error, field_error, ColumnNotFoundError
from .server_config import Server
from ..sql.schema import ORMBase
from ..socket.protocol import MESSAGE_KEYS, format_map, MessageTypes


E = TypeVar('E', bound=Enum)
HEX_REGEX = r'^#[0-9a-fA-F]{6}$'


# === General Funcs ===

def validate_field(
                   field: str,
                   field_val: Any,
                   expected_type: Any
                  ) -> None:
    """
    Validates a field's type

    Parameters
    ----------
    field : str
        The name of the field (for error messages)
    field_val : Any
        The value to validate
    expected_type : Any
        The expected type of the value

    Raises
    ------
    TypeError
        If `value` is not of type `expected_type`

    Notes
    -----
    - If `field` is not a non-empty str, I will gut you like a fish
    """
    if not isinstance(field_val, expected_type):
        raise arg_error(field, field_val, expected_type)


def validate_enum(
                  field: str,
                  field_val: Any,
                  enum_type: type[E]
                 ) -> E:
    """
    Validates `field_val` is a member of `enum_type`

    Parameters
    ----------
    field : str
        The name of the field (for error messages)
    field_val : Any
        The value to validate
    enum_type : type[Enum]
        The enum class to check against

    Returns
    -------
    E
        The validated enum member

    Raises
    ------
    TypeError
        If `field_val` is not a member of `enum_type`

    Notes
    -----
    - If `field` is not a non-empty str, I will gut you like a fish
    - If `enum_type` is not an Enum, I will gut you like a fish
    """
    try:
        return enum_type(field_val)
    except ValueError as e:
        valid_vals = [m.value for m in enum_type]
        raise field_error(
            field, field_val,
            f'member of {enum_type.__name__} ({valid_vals})'
        ) from e


def validate_str(field: str, field_val: str) -> None:
    """
    Validates a string (field_val) is indeed a string,
    with non-empty and whitespace checks

    Parameters
    ----------
    field : str
        The name of the field (for error messages)
    field_val : str
        The string to validate

    Raises
    ------
    TypeError
        If `field` is not a str
    FieldError
        If `field_val` is empty or whitespace-only

    Notes
    -----
    - If `field` is not a non-empty str, I will gut you like a fish
    """
    validate_field(field, field_val, str)

    if not field_val or field_val.isspace():
        raise field_error(field, field_val, 'non-empty str')

def validate_hex(field: str, field_val: str) -> None:
    """
    Validates a string (field_val) is a valid hex colour code

    Parameters
    ----------
    field : str
        The name of the field (for error messages)
    field_val : str
        The string to validate

    Raises
    ------
    TypeError
        If `field` is not a str
    FieldError
        If `field_val` is not a valid hex colour code

    Notes
    -----
    - If `field` is not a non-empty str, I will gut you like a fish
    """
    validate_str(field, field_val)

    if not fullmatch(HEX_REGEX, field_val):
        raise field_error(
            field, field_val, 'valid hex colour code (eg. #1A2B3C)'
        )

def validate_int(
                  field: str,
                  field_val: int,
                  non_negative: bool = True,
                  positive: bool = True
                 ) -> None:
    """
    Validates an integer is indeed an integer,
    with optional positivity and non-zero checks

    Parameters
    ----------
    field : str
        The name of the field (for error messages)
    field_val : int
        The integer to validate
    non_negative : bool = True
        Whether to check if the integer is non-negative
    positive : bool = True
        Whether to check if the integer is positive

    Raises
    ------
    TypeError
        If `field_val` is not an int
    ValueError
        - If `positive` is True and `field_val` is not positive
        - If `non_negative` is True and `field_val` is zero

    Notes
    -----
    - If `field` is not a non-empty str, I will gut you like a fish
    - If `positive` and `non_negative` are not bools, I will gut you like a fish
    - If anything but `field_val` is invalid, I will gut you like a fish
    """
    validate_field(field, field_val, int)

    if positive and field_val <= 0:
        raise field_error(field, field_val, 'positive int (> 0)')
    elif non_negative and field_val < 0:
        raise field_error(field, field_val, 'non-negative int (>= 0)')


def validate_dict(
                  field: str,
                  field_val: dict[str, Any],
                  format: type | None = None
                 ) -> None:
    """
    Validates a dictionary is indeed a dictionary with str keys,
    and optionally matches a TypedDict format

    Parameters
    ----------
    field : str
        The name of the field (for error messages)
    field_val : dict[str, Any]
        The dictionary to validate
    format : TypedDict | None = None
        The expected TypedDict (keys and value types)

    Raises
    ------
    TypeError
        - If `field_val` is not a dict
        - If all keys in `field_val` are not str

    Notes
    -----
    - If `field` is not a non-empty str, I will gut you like a fish
    """
    validate_field(field, field_val, dict)

    val_keys = list(field_val.keys())

    for key in val_keys:
        validate_field(f'{field} key', key, str)

    if format:
        # Get type hints from TypedDict
        expected_annotations = get_type_hints(format)
        expected_keys = list(expected_annotations.keys())

        if set(val_keys) != set(expected_keys):
            raise field_error(
                f'{field} keys', val_keys,
                f'keys to match {expected_keys}'
            )

        # validate value types
        for key, expected_type in expected_annotations.items():
            validate_field(
                f'{field}[{key!r}]',
                field_val[key],
                expected_type
            )

def validate_msg(
                 msg: dict[str, Any]
                ) -> dict[str, Any]:
    """
    Validates a message has the correct data format

    Parameters
    ----------
    msg : Message
        The message to validate

    Raises
    ------
    TypeError
        If `msg` is not a dict with str keys
    ValueError
        - If `msg` keys don't match the expected format
        - If `msg['type']` is not a valid MessageTypes member
        - If `msg['data']` does not match the expected format
    """
    validate_dict('message', msg)

    if set(msg.keys()) != MESSAGE_KEYS:
        raise field_error(
            'message keys', list(msg.keys()),
            f'keys to match {list(MESSAGE_KEYS)}'
        )

    # validate & convert to enum
    msg_type = validate_enum("msg['type']", msg['type'], MessageTypes)

    # get expected data format
    expected_format = format_map.get(msg_type)
    if not expected_format:
        raise field_error(
            'msg[type]', msg['type'],
            f'valid MessageTypes member'
        )

    # validate data format
    validate_dict('msg', msg, expected_format)

    return msg


# === Socket Funcs ===

def validate_data(data: Any) -> None:
    """
    Validates `data` is not None or empty
    (for socket send/recv)

    Parameters
    ----------
    data : Any
        The data to validate

    Raises
    ------
    ValueError
        If `data` is None or empty
    """
    if data is None or len(data) == 0:
        raise ValueError('No data provided')

def validate_conn(conn: socket.socket) -> None:
    """
    Validates `conn` is a socket.socket instance

    Parameters
    ----------
    conn : socket.socket
        The socket connection to validate

    Raises
    ------
    TypeError
        If `conn` is not a socket.socket instance
    """
    validate_field('conn', conn, socket.socket)



# === Server Funcs ===

def validate_f_type(f_type: str) -> bool:
    """
    Validates `f_type` is in `Server.VALID_F_TYPES`

    Parameters
    ----------
    f_type : str
        The file type to validate

    Returns
    -------
    bool
        True if `f_type` is valid, False otherwise
    """
    return f_type in Server.VALID_F_TYPES


def validate_model_field(
                         model_class: type[ORMBase],
                         field_name: str
                        ) -> None:
        """
        Validates `field_name` is a valid field of `model_class`

        Parameters
        ----------
        model_class : type[Base]
            The Pydantic model class to validate against
        field_name : str
            The field name to validate

        Raises
        ------
        TypeError
            If `field_name` is not a str
        ValueError
            If `field_name` is empty or whitespace-only
        ColumnNotFoundError
            If `field_name` is not a valid attribute of `model_class`
        """
        validate_str('field_name', field_name)

        if not hasattr(model_class, field_name):
            raise ColumnNotFoundError(field_name, model_class.__tablename__)





# === Exports ===

__all__ = [
           'validate_field',
           'validate_enum',

           'validate_str',
           'validate_hex',
           'validate_int',
           'validate_dict',
           'validate_msg',

           'validate_data',
           'validate_conn',

           'validate_f_type',
           'validate_model_field'
          ]
