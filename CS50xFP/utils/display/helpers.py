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
  print(string.center(SIZE), end=end, flush=flush)
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
    '''
    Clear the screen
    '''
    # OS is windows
    if name == 'nt':
        system("cls")
    # OS is mac or linux (or any other I guess, it's an else statement...)
    else:
        system("clear")


def timestamp() -> str:
  '''
  Gets the current timestamp

  Format: YYYY/MM/DD - HH/MM/SS
  '''
  curr_dt = datetime.now()
  return curr_dt.strftime("%Y/%m/%d - %H/%M/%S")

