"""
Useful validation functions

Contains
--------

"""

from typing import Any

from .exceptions import ArgumentError, FieldError



def _validate_field(
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
        raise ArgumentError(field, field_val, expected_type)


def _validate_str(field: str, field_val: str) -> None:
    """
    Validates that a string (field_val) is indeed a string,
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
        If `field_val` is an empty or whitespace-only string

    Notes
    -----
    - If `field` is not a non-empty str, I will gut you like a fish
    """
    _validate_field(field, field_val, str)

    if not field_val or field_val.isspace():
        raise FieldError(field, field_val, 'non-empty str')

def _validate_int(
                  field: str,
                  field_val: int,
                  non_negative: bool = True,
                  positive: bool = True
                 ) -> None:
    """
    Validates that an integer is indeed an integer,
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
        - If `nonzero` is True and `field_val` is zero

    Notes
    -----
    - If `field` is not a non-empty str, I will gut you like a fish
    - If `positive` and `nonzero` are not bools, I will gut you like a fish
    - If anything but `field_val` is invalid, I will gut you like a fish
    """
    _validate_field(field, field_val, int)

    if non_negative and field_val <= 0:
        raise FieldError(field, field_val, 'non-negative int')
    if positive and field_val < 0:
        raise FieldError(field, field_val, 'positive int')



# === Exports ===

__all__ = [
           '_validate_field',
           '_validate_str',
           '_validate_int'
          ]
