"""
Helpers for printing piped lines and `print_piped_line()`
"""

# === Imports ===

from ...config import BAR_WIDTH, LEFT_PADDING
from ....sql.exceptions import FieldError

from rich.console import Console
from rich.text import Text
from typing import Literal



# === Helpers ===

# Text formatting
def _format_label_val_text(
                           string: str,
                           colour: str | None = None,
                          ) -> tuple[Text, Text | str]:
    """
    Formats text for piped line printing

    Parameters
    ----------
    string : str
        Text to format
    colour : str or None, optional
        hex colour code or Rich colour name for text styling.
        If None, uses default styling.

    Returns
    -------
    Label : Text
        Formatted label text
    Value : Text or str
        Formatted value text

    Raises
    ------
    ValueError
        If `string` does not contain a colon

    Examples
    --------
    >>> _format_label_val_text('Label: Value', '#FF0000')
    (Text('Label:', style='bold'), Text(' Value', style='#FF0000'))

    >>> _format_label_val_text('Label: Value')
    (Text('Label:', style='bold'), ' Value')
    """
    # formatting only applies after the colon
    split_string = string.split(':', 1)

    # input validation
    if len(split_string) != 2:
        raise FieldError('string', string, 'Must contain a colon.')

    # first string is bold
    str_1 = Text(f'{split_string[0]}:', 'bold')

    # now second string
    if split_string[1].strip() in ['[DATA EXPUNGED]', 'None']:
        str_2 = Text(split_string[1], 'dim')
    elif colour:
        str_2 = Text(split_string[1], colour)
    else:
        str_2 = split_string[1]

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


    available_space = content_width - len(string)

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
                  ) -> tuple[str, str]:
    if cols == 2:
        left_sep  = '║' if side == 'l' else '║║'
    elif cols == 3:
        left_sep  = '║'
    else: # validation
        raise FieldError('cols', cols, '2 or 3')

    right_sep = '║' if side == 'r' else '' # same for 2 & 3 cols

    return left_sep, right_sep



# === Main Functions ===

def print_centered_line(console: Console,
                        string: str,
                        side: Literal['l', 'r', 'c'],
                        colour: str | None = None,
                        content_width: int = BAR_WIDTH,
                       ) -> None:
    """
    Renders a formatted centered line to the console
    String must contain a colon and fit in content width

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
    colour : str or None, optional
        hex colour code or Rich colour name for text styling.
        If None, uses default styling.
    content_width : int, default=BAR_WIDTH
        Width of the line content area

    Raises
    ------
    ValueError
        - If `side` is not 'l', 'r', or 'c'
        - If `string` does not contain a colon
        - If `string` is too long to fit in content width

    Example
    -------
    >>> print_centered_line(console, 'Label: Value', 'l', content_width=28)
    '        Label: Value        '  # printed to console
    """

    # calculate spacing
    left_padding, right_padding = _calc_spacing(string, content_width, side)

    # format text
    label_text, value_text = _format_label_val_text(string, colour)

    # print line
    console.print(
                  left_padding, label_text,
                  value_text, right_padding,
                  end='', sep=''
                 )


def print_piped_line(console: Console,
                     string: str,
                     side: Literal['l', 'r', 'c'],
                     colour: str | None = None,
                     content_width: int = BAR_WIDTH,
                     cols: Literal[2, 3] = 2
                    ) -> None:
    """
    Renders a piped, formatted centered line to the console
    String must contain a colon and fit in content width

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
    colour : str or None, optional
        hex colour code or Rich colour name for text styling.
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
        - If `string` does not contain a colon
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

    print(left_sep, end='')

    print_centered_line(
                        console, string, side,
                        colour, content_width
                       )

    print(right_sep, end = ('\n' if side == 'r' else ''))
