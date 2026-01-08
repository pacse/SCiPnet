"""
Helpers for display functions

Contains
--------
- printc()
- print_lines()
- print_md()
- print_md_title()

- clear()
- timestamp()
"""

from ..general.display_config import Terminal

from os import name, system
from datetime import datetime
from rich.console import Console
from rich.markdown import Markdown as Md
from ..general.validation import validate_str, validate_field


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
    validate_field('string', string, str)
    validate_field('end', end, str)
    validate_field('flush', flush, bool)
    validate_field('truncate', truncate, bool)
    validate_field('overwrite', overwrite, bool)

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
    validate_field('lines', lines, list)
    for line in lines:
        validate_field('lines item', line, str)

    # print
    for line in lines:
        printc(line)

def print_md(
             text: str,
             console: Console
            ) -> None:
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
    validate_str('text', text)
    validate_field('console', console, Console)

    console.print(Md(text))

def print_md_title(
                   title: str,
                   text: str,
                   console: Console
                  ) -> None:
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

    validate_str('title', title)
    validate_str('text', text)

    print_md(f'## {title}\n{text}', console)


def clear() -> None:
    """
    Clears the screen
    """

    # determine clear command
    if name == 'nt':       # OS is windows
        command = 'cls'
    else:                  # OS is mac or linux (or any other I guess,
        command = 'clear'  #                     it's an else statement...)

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
