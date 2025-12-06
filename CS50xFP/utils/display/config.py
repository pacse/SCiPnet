"""
Display configuration settings and constants

Included in *:
- MIN_TERMINAL_WIDTH
- BAR_WIDTH
- BOX_SIZE
- SIZE
- CLEAR_LVL_COLOURS
- CONT_CLASS_COLOURS

Excluded from *:
- all imports
- HEX_CODE_REGEX
- OTHER_CONT_CLASS
"""

from collections import defaultdict

# disable markdown_it logging
import logging
logging.getLogger('markdown_it').setLevel(logging.WARNING)


# terminal size calculation
def _get_term_width() -> int:
    """gets terminal width, adjusted to be even"""
    try:
        from os import get_terminal_size
        width = get_terminal_size().columns

        width = width - (width % 2) # make even

        # validate size
        if width < MIN_TERM_WIDTH:
            raise RuntimeError(
                f'Terminal too small: {width} columns '
                f'(minimum required: {MIN_TERM_WIDTH})'
            )

    except Exception as e:
        raise RuntimeError(
            f'Could not get terminal size:\n{e}'
        ) from e

    return width


# === Mayuk size constants ===

MIN_TERM_WIDTH = 120
"""Minimum terminal width required for proper display"""

BAR_WIDTH = 58
"""Width of text areas used in user/site/SCP/MTF display"""

ACS_TOP_BAR_WIDTH = 32
"""Width of left/right text areas of the ACS top bar"""

BOX_SIZE = 35 # fits most messages nicely
"""Default box size for boxed messages"""

SIZE = _get_term_width()
"""Terminal width in columns, adjusted to be even"""

LEFT_PADDING = ' ' * ((SIZE - MIN_TERM_WIDTH) // 2)
"""Spaces to center 120 char content in terminal"""



# === Colour Configurations ===

CLEAR_LVL_COLOURS = [
    '',
    '#009F6B',
    '#0087BD',
    '#FFD300',
    '#FF6D00',
    '#C40233',
    '#850005'
]
"""
Hex colour codes used in clearance level rendering

index is level
(eg, COLOURS[1] is used for clearance level 1)
"""


OTHER_CONT_CLASS = 'dim'  # grey for all containment classes
"""Hex colour code used for containment classes not in CONT_CLASS_COLOURS"""

CONT_CLASS_COLOURS = defaultdict(
    lambda: OTHER_CONT_CLASS,
    {
        'Safe': CLEAR_LVL_COLOURS[1],
        'Euclid': CLEAR_LVL_COLOURS[3],
        'Keter': CLEAR_LVL_COLOURS[5],
    }
)
"""
Hex colour codes used in containment class & secondary class rendering

ALWAYS USE `.get()` TO ACCESS THIS DICT

keys are containment classes
(eg, CONT_CLASS_COLOURS.get('Safe') is used for Safe class)
"""


# what's importable
__all__ = [
    'MIN_TERM_WIDTH',
    'BAR_WIDTH',
    'BOX_SIZE',
    'SIZE',
    'CLEAR_LVL_COLOURS',
    'CONT_CLASS_COLOURS'
]
