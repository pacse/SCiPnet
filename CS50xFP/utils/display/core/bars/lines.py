"""
Helpers for printing piped lines and `print_piped_line()`

Contains
--------
- format_centered_text: Formats centered text for piped line printing
- print_centered_line: Renders centered text to console
- print_piped_line: Renders piped, centered text to console
"""

# === Imports ===

from ...config import (BAR_WIDTH, LEFT_PADDING, OTHER_CONT_CLASS,
                       PLACEHOLDER, SPECIAL_TEXTS, ACTIVE_TEXT,
                       DIGIT_REGEX, QUOTED_REGEX)
from ....sql.exceptions import FieldError

from rich.console import Console
from rich.text import Text
from typing import Literal



# === Helpers ===

# Text formatting
def default_formatting(string: str) -> Text:
    """
    Applies default formatting to string:
    - digits are styled as 'cyan bold'
    - text in double quotes is styled as 'green'
    - special cases:
      - '[DATA EXPUNGED]', 'None', & 'Inactive' are styled with OTHER_CONT_CLASS
      - 'Active' is styled as 'green'

    Parameters
    ----------
    string : str
        Text to format

    Returns
    -------
    Text
        Formatted text
    """
    t = Text(string)

    # special cases
    if string.strip() in SPECIAL_TEXTS:
        t.stylize(OTHER_CONT_CLASS)
    elif string.strip() == ACTIVE_TEXT:
        t.stylize('green')

    # normal formatting
    else:
        t.highlight_regex(DIGIT_REGEX, 'cyan bold')  # digit coloring
        t.highlight_regex(QUOTED_REGEX, 'green')     # text coloring

    return t

def _format_label_val_text(
                           string: str,
                           style: str | None = None,
                          ) -> tuple[Literal[''] | Text | str, Text | str]:
    """
    Formats text for piped line printing

    If string contains a colon, splits into label (bolded) and value (styled).

    Parameters
    ----------
    string : str
        Text to format
    style : str or None, optional
        string to pass to Text for styling.
        If None, uses default styling.

    Returns
    -------
    Label : Literal[''] or Text or str
        Formatted label text (bolded), or empty string if no label, or string if brackets present.
    Value : Text or str
        Formatted value text. If no style provided, returns unstyled str.
        ('[DATA EXPUNGED]', 'None', & 'Inactive' are styled with OTHER_CONT_CLASS.)

    Examples
    --------
    >>> _format_label_val_text('Label: Value', '#FF0000')
    (Text('Label:', style='bold'), Text(' Value', style='#FF0000'))

    >>> _format_label_val_text('Value', 'dim')
    Text('Value', style='dim')
    """

    # replace escaped colons
    string = string.replace('\\:', PLACEHOLDER)

    # formatting only applies after the colon
    parts = string.split(':', 1)

    # restore escaped colons
    parts = [p.replace(PLACEHOLDER, ':') for p in parts]

    # check str length
    if len(parts) == 1:
        if style:
            return '', Text(parts[0], style)

        else:
            return '', default_formatting(parts[0])


    # first string is bold
    str_1 = Text(f'{parts[0]}:', 'bold')

    # now second string
    if style:
        str_2 = Text(parts[1], style)
    else:
        str_2 = default_formatting(parts[1])

    return (str_1, str_2)


# spacing calculations
def _calc_spacing(
                  string: str,
                  content_width: int,
                  side: Literal['l', 'r', 'c']
                 ) -> tuple[str, str]:
    """
    Calculates spacing for piped line printing

    Parameters
    ----------
    string : str
        Text to print
    content_width : int
        Width of the line content area
    side : {'l', 'r', 'c'}
        Which side of the bar the line is on

    Returns
    -------
    left_padding : str
        Spaces before text
    right_padding : str
        Spaces after text

    Raises
    ------
    ValueError
        - If `side` is not 'l', 'r', or 'c'
        - If string is too long to fit in content_width

    Examples
    --------
    >>> _calc_spacing('Label: Value', 30, 'l')
    (' ' * 9, ' ' * 9)
    >>> _calc_spacing('Label: 01', 30, 'r')
    (' ' * 10, ' ' * 11)
    """

    # input validation
    if side not in ['l', 'r', 'c']:
        raise FieldError('side', side, "'l', 'r', or 'c'")


    # calculate available space without escape chars
    available_space = content_width - len(string.replace('\\', ''))

    if available_space < 0:
        raise FieldError(
            'string', string,
            f'string to fit in content_width ({content_width})'
        )

    padding = ' ' * (available_space // 2)
    extra = ' ' * (available_space % 2)

    if side == 'l':
        return f'{padding}{extra}', padding

    else:
        return padding, f'{padding}{extra}'


# determine column seperators
def _get_pipe_seps(cols: Literal[2, 3],
                   side: Literal['l', 'r', 'c']
                  ) -> tuple[Literal['║', '║║'], Literal['║', '']]:
    if cols == 2:
        left_sep  = '║' if side == 'l' else '║║'
    elif cols == 3:
        left_sep  = '║'
    else: # validation
        raise FieldError('cols', cols, '2 or 3')

    right_sep = '║' if side == 'r' else '' # same for 2 & 3 cols

    return left_sep, right_sep



# === Main Functions ===

def format_centered_text(
                         string: str,
                         side: Literal['l', 'r', 'c'],
                         style: str | None = None,
                         content_width: int = BAR_WIDTH,
                         right_sep: Literal['║', ''] = '║'
                        ) -> tuple[str, Literal[''] | Text | str,
                                   Text | str, str, Literal['║','']]:
    """
    Formats centered text

    Parameters
    ----------
    string : str
        Text to print
    side : {'l', 'r', 'c'}
        Which side of the bar the line is on: (affects placement of extra space if needed)
    style : str or None, optional
        string to use for text styling.
        If None, uses default styling.
    content_width : int, default=BAR_WIDTH
        Width of the line content area
    right_sep : {'║', ''}, default='║'
        Right separator

    Returns
    -------
    left_padding : str
        Spaces before text
    label_text : Text or Literal[''] or str
        Formatted label text (bolded), or empty string if no label, or string if brackets present.
    value_text : Text or str
        Formatted value text. If no style provided, returns unstyled str.
        ('[DATA EXPUNGED]', 'None', & 'Inactive' are styled with OTHER_CONT_CLASS.)
    right_padding : str
        Spaces after text
    right_sep : Literal['║', '']
        Right separator
    """

    left_padding, right_padding = \
        _calc_spacing(string, content_width, side)
    label_text, value_text = _format_label_val_text(string, style)

    return left_padding, label_text, value_text, right_padding, right_sep


def print_centered_line(console: Console,
                        string: str,
                        side: Literal['l', 'r', 'c'],
                        style: str | None = None,
                        content_width: int = BAR_WIDTH,
                       ) -> None:
    """
    Renders a formatted centered line to the console
    String must fit in content width

    Parameters
    ----------
    console : Console
        Console to print to
    string : str
        Text to print
    side : {'l', 'r', 'c'}
        Which side of the bar the line is on: (affects placement of extra space if needed)

        - 'l': left side
        - 'r': right side
        - 'c': center
    style : str or None, optional
        string to use for text styling.
        If None, uses default styling.
    content_width : int, default=BAR_WIDTH
        Width of the line content area

    Raises
    ------
    ValueError
        - If `side` is not 'l', 'r', or 'c'
        - If `string` is too long to fit in content width

    Example
    -------
    >>> print_centered_line(console, 'Label: Value', 'l', content_width=28)
    '        Label: Value        '  # printed to console
    """

    # Generate and render line
    console.print(
                  *format_centered_text(
                                        string,
                                        side,
                                        style,
                                        content_width,
                                        '' # no right sep
                                       ),
                  end='', sep=''
                 )


def print_piped_line(console: Console,
                     string: str,
                     side: Literal['l', 'r', 'c'],
                     style: str | None = None,
                     content_width: int = BAR_WIDTH,
                     cols: Literal[2, 3] = 2
                    ) -> None:
    """
    Renders a piped, formatted centered line to the console
    String must fit in content width

    Parameters
    ----------
    console : Console
        Console to print to
    string : str
        Text to print
    side : {'l', 'r', 'c'}
        Which side of the bar the line is on: (affects placement of extra space if needed)
        - 'l': left side
        - 'r': right side
        - 'c': center
    style : str or None, optional
        string to use for text styling.
        If None, uses default styling.
    content_width : int, default=BAR_WIDTH
        Width of the line content area
    cols : {2, 3}, default=2
        Number of columns in the bar:
        - 2: left and right sides
        - 3: left, center, and right sides

    Raises
    ------
    ValueError
        - If `side` is not 'l', 'r', or 'c'
        - If `string` is too long to fit in content width
        - If `cols` is not 2 or 3
        - if `side` is 'c' and `cols` is 2

    Example
    -------
    >>> print_piped_line(console, 'Label: Value', 'l', content_width=28)
    '║        Label: Value        '  # printed to console
    """

    # validation
    if cols == 2 and side == 'c':
        raise FieldError('side', side, "'l' or 'r' for 2-column bars")

    left_sep, right_sep = _get_pipe_seps(cols, side)

    if side == 'l':
        left_sep = f'{LEFT_PADDING}{left_sep}'

    console.print(
                  left_sep,
                  *format_centered_text(
                                        string,
                                        side,
                                        style,
                                        content_width,
                                        right_sep
                                       ),
                  sep='', end = ('\n' if side == 'r' else '')
                 )
