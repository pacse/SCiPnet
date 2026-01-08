"""
Box generators for displays

Contains
--------
- basic_box: Prints a multiline box
- basic_box_with_text: Prints a multiline box with text below
"""

from ..helpers import print_lines, printc, timestamp
from ...general.display_config import Boxes
from ...general.exceptions import field_error
from ...general.validation import validate_field, validate_str



def basic_box(lines: list[str]) -> None:
    """
    Prints a formatted box with the provided lines centered inside

    Parameters
    ----------
    lines : list[str]
        The lines to be displayed inside the box

    Raises
    ------
    ValueError
        - If `lines` is empty
        - If longest line is greater than `Boxes.MAX_TEXT_SIZE - Boxes.PADDING`
    TypeError
        If any element in `lines` is not a string
    """
    validate_field('lines', lines, list)
    for line in lines:
        validate_str('lines item', line)

    # determine box width
    max_line_len = max(len(line) for line in lines)
    box_width = max(Boxes.DEF_TEXT_SIZE, max_line_len + Boxes.PADDING)  # ensure box has padding

    # check width
    if box_width > Boxes.MAX_TEXT_SIZE:
        raise field_error(
            'line length', max_line_len,
            ('longest line to be '
             f'{Boxes.MAX_TEXT_SIZE - Boxes.PADDING} chars or fewer')
        )

    # === Render ===

    # reused strs
    TOP_BOTTOM = '═' * box_width
    EMPTY = f'║{' ' * box_width}║'

    print_lines([
        '',
        f'╔{TOP_BOTTOM}╗',
        EMPTY,
        *[f'║{line:^{box_width}}║' for line in lines],
        EMPTY,
        f'╚{TOP_BOTTOM}╝',
        ''
    ])


def basic_box_with_text(
                        box_text: list[str],
                        desc_text: list[str],
                        RAISA_log: bool = True
                       ) -> None:
    """
    Prints a formatted box with `box_text` centered
    inside followed by `desc_text` centered below the box

    If RAISA_log is True, says the action was logged
    to RAISA @ the current timestamp

    Parameters
    ----------
    box_text : list[str]
        The lines to be displayed inside the box
    desc_text : list[str]
        Description lines to be displayed below the box
    RAISA_log : bool, default=True
        Whether to indicate logging to RAISA, by default True

    Raises
    ------
    ValueError
        If `box_text` or `desc_text` is empty
    TypeError
        If any element in `box_text` or `desc_text` is not a string
    """
    # box_text validated in basic_box()
    validate_field('desc_text', desc_text, list)
    for line in desc_text:
        validate_str('desc_text item', line)
    validate_field('RAISA_log', RAISA_log, bool)

    # render
    basic_box(box_text)
    print_lines(desc_text)
    if RAISA_log:
        printc(f'Logged to RAISA at {timestamp()}')

    print()


def fancy_box(lines: list[str]) -> None:
    """
    Prints a fancy box with the provided lines centered inside
    """
    validate_field('lines', lines, list)
    for line in lines:
        validate_field('lines item', line, str)

    print_lines([
        ''
        '██▀▀▀██▀▀▀██▀▀▀██▀▀▀██▀▀▀██▀▀▀██▀▀▀██▀▀▀██▀▀▀██▀▀▀██▀▀▀██▀▀▀██▀▀▀██▀▀▀██▀▀▀██▀▀▀██▀▀▀██▀▀▀██▀▀▀██▀▀▀██▀▀▀██▀▀▀██',
        '█████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓█████',
        '██ ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ ██',
        '',
        *lines,
        '',
        '██ ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ ██',
        '█████ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ █████',
        '██▄▄▄██▄▄▄██▄▄▄██▄▄▄██▄▄▄██▄▄▄██▄▄▄██▄▄▄██▄▄▄██▄▄▄██▄▄▄██▄▄▄██▄▄▄██▄▄▄██▄▄▄██▄▄▄██▄▄▄██▄▄▄██▄▄▄██▄▄▄██▄▄▄██▄▄▄██',
        ''
    ])


def fancy_box_with_text(
                        box_text: list[str],
                        desc_text: list[str],
                        raisa_log: bool = True
                       ) -> None:
    """
    Prints a fancy box with `box_text` centered
    inside followed by `desc_text` centered below the box

    Parameters
    ----------
    box_text : list[str]
        The lines to be displayed inside the box
    desc_text : list[str]
        Description lines to be displayed below the box

    Raises
    ------
    ValueError
        - If `box_text` or `desc_text` is empty
    TypeError
        - If any element in `box_text` or `desc_text` is not a string
    """
    # box_text validated in fancy_box()
    validate_field('desc_text', desc_text, list)
    for line in desc_text:
        validate_str('desc_text item', line)

    # render
    fancy_box(box_text)
    print_lines(desc_text)
    if raisa_log:
        printc(f'Logged to RAISA at {timestamp()}')

    print()
