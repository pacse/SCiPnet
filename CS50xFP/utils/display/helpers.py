"""
Helpers for display functions

Contains
--------
- check_type_and_empty_str()

- printc()
- print_lines()
- print_md()
- print_md_title()

- clear()
- timestamp()
"""

from .config import Terminal

from os import name, system
from datetime import datetime
from rich.console import Console
from rich.markdown import Markdown as Md



def check_type_and_empty_str(var: str, var_name: str) -> bool:
    """
    checks if `var` is a string and non-empty

    Parameters
    ----------
    var : str
        variable to check
    var_name : str
        name of variable to use in error messages

    Raises
    ------
    TypeError
        If `var` is not a string
    ValueError
        If `var` is empty or whitespace

    Returns
    -------
    bool
        True if `var` is a non-empty string
    """
    if not isinstance(var, str):
        raise TypeError(f'`{var_name}` must be a string')
    if not var or var.isspace():
        raise ValueError(f'`{var_name}` must be a non-empty string')

    return True


def printc(
           string: str,
           end: str = '\n',
           flush: bool = False,
           truncate: bool = True,
           overwrite: bool = False
          ) -> None:
    """
    Prints `string` centered to the terminal size
    (Does not handle ANSI codes or wide unicode chars)

    Parameters
    ----------
    string : str
        string to print
    end : str
        char to end line with
    flush : bool
        whether to forcibly flush `string`
    truncate : bool
        whether to truncate `string` if longer than terminal size
    overwrite : bool
        whether to overwrite the current line instead of printing a new one (carriage return)
    """

    # validation
    for v_name, v in [
                      ('string', string),
                      ('end', end)
                     ]:
        if not isinstance(v, str):
            raise TypeError(f'Expected `{v_name}` to be type str, '
                            f'got {type(v).__name__}')

    for v_name, v in [
                      ('flush', flush),
                      ('truncate', truncate),
                      ('overwrite', overwrite)
                     ]:
        if not isinstance(v, bool):
            raise TypeError(f'Expected `{v_name}` to be type bool, '
                            f'got {type(v).__name__}')

    # print
    if string == '':
        print(end=end, flush=flush)
        return

    elif truncate and len(string) > Terminal.SIZE:
        string = f'{string[:Terminal.SIZE-3]}...'

    if overwrite:
        print(f'\r{string:^{Terminal.SIZE}}', end=end, flush=flush)
    else:
        print(f'{string:^{Terminal.SIZE}}', end=end, flush=flush)

def print_lines(
                lines: list[str]  # possible later: accept generators
               ) -> None:
    """
    printc's all lines provided

    Parameters
    ----------
    lines : list[str]
        strings to pass to printc

    Raises
    ------
    TypeError
        If `lines` is not a list of strings
    """

    # validation
    if not isinstance(lines, list):
        raise TypeError('Expected `lines` to be type list, '
                        f'received {type(lines).__name__}')
    if not all(isinstance(line, str) for line in lines):
        raise TypeError('Expected all items in `lines` to be type str')

    if not lines:
        return


    # print
    for line in lines:
        printc(line)

def print_md(text: str, console: Console) -> None:
    """
    Prints markdown text to the console

    Parameters
    ----------
    text : str
        markdown text to print
    console : Console
        rich console to print to

    Raises
    ------
    TypeError
        - If `text` is not a string
        - If `console` is not a rich Console instance
    ValueError
        If `text` is an empty string

    Notes
    -----
    Calls `console.print(Md(`text`))`
    """
    check_type_and_empty_str(text, 'text')

    if not isinstance(console, Console):
        raise TypeError('`console` must be a rich Console instance')

    console.print(Md(text))

def print_md_title(title: str, text: str, console: Console) -> None:
    """
    Prints markdown text with a title to the console

    Parameters
    ----------
    title : str
        title of the markdown section
    text : str
        markdown text to print
    console : Console
        rich console to print to

    Raises
    ------
    TypeError
        - If `title` is not a string
        - If `text` is not a string
        - If `console` is not a rich Console instance
    ValueError
        - If `title` is an empty string
        - If `text` is an empty string

    Notes
    -----
    - Title is printed as a level 2 markdown header
    - Calls `print_md(f'## {title}\n{text}', console)`
    """

    check_type_and_empty_str(title, 'title')
    check_type_and_empty_str(text, 'text')

    print_md(f'## {title}\n{text}', console)


def clear() -> None:
    """
    Clears the screen
    """

    # determine clear command
    if name == 'nt':       # OS is windows
        command = 'cls'
    else:                  # OS is mac or linux (or any other I guess, it's an else statement...)
        command = 'clear'

    # execute clear command
    try:
        result = system(command)

    # error handling
    except OSError as e:
        raise OSError(f'Clear command ({command!r}) failed: {e}') from e
    if result != 0:
        raise OSError(
            f'Clear command ({command!r}) failed with exit code {result}'
        )


def timestamp() -> str:
    """
    Gets the current timestamp (uses local timezone)

    Only for use client-side as server uses UTC

    Returns
    -------
    current_datetime : str
        The current datetime formatted as: YYYY/MM/DD - HH:MM:SS
        Example: 2024/06/01 - 14:30:15
    """
    return datetime.now().strftime('%Y/%m/%d - %H:%M:%S')
