"""
Helpers for display functions

Contains
--------
- printc()
- print_lines()
- clear()
- timestamp()
"""

from .config import SIZE

from os import name, system
from datetime import datetime



def printc(
           string: str,
           end: str = '\n',
           flush: bool = False
          ) -> None:
    """
    Prints `string` centered to the terminal size

    Parameters
    ----------
    string : str
        string to print
    end : str
        char to end line with
    flush : bool
        whether to forcibly flush `string`
    """

    # validation
    if not isinstance(string, str):
        raise TypeError('Expected `string` to be type str,'
                        f'received {type(string).__name__}')
    if not isinstance(end, str):
        raise TypeError('Expected `end` to be type str,'
                        f'received {type(end).__name__}')
    if not isinstance(flush, bool):
        raise TypeError('Expected `flush` to be type bool'
                        f'received {type(flush).__name__}')

    # print
    print(f'{string:^{SIZE}}', end=end, flush=flush)


def print_lines(
                lines: list[str]
               ) -> None:
    """
    printc's all lines provided

    lines : list[str]
        strings to pass to printc
    """

    for line in lines:
        if line == '':
            print()
        else:
            printc(line)


def clear() -> None:
    """
    Clears the screen
    """
    # OS is windows
    if name == 'nt':
        command = 'cls'
    # OS is mac or linux (or any other I guess, it's an else statement...)
    else:
        command = 'clear'

    try:
        system(command)
    except Exception as e:
        raise OSError(f'Failed to execute clear: {e}') from e


def timestamp() -> str:
    """
    Gets the current timestamp (uses local timezone)

    Only for use client-side as server uses UTC

    Returns
    -------
    current_datetime : str
        The curent datetime formatted as: YYYY/MM/DD - HH/MM/SS
    """
    curr_dt = datetime.now()
    return curr_dt.strftime(r'%Y/%m/%d - %H/%M/%S')

