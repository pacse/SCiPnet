"""
Display configuration settings and constants

Contains
--------
- MIN_TERMINAL_WIDTH
- BAR_WIDTH
- ACS_TOP_BAR_WIDTH
- DEFAULT_BOX_SIZE
- MAX_BOX_SIZE
- SIZE
- LEFT_PADDING

- CLEAR_LVL_COLOURS
- CONT_CLASS_COLOURS
- OTHER_CONT_CLASS
- CONT_CLASS_COLOURS

- PLACEHOLDER
- SPECIAL_TEXTS
- ACTIVE_TEXT
- DIGIT_REGEX
- QUOTED_REGEX
"""

from collections import defaultdict

# disable markdown_it logging
# (causes problems with rich if not disabled)
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
"""
Minimum terminal width required for proper display
(largest fixed-width display is 120 chars)
"""

BAR_WIDTH = 58
"""Width of text areas used in user/site/SCP/MTF display"""

ACS_TOP_BAR_WIDTH = [32, 54, 32]
"""Width of text areas of the top bar for ACS & MTF (left, center, right)"""

DEFAULT_BOX_SIZE = 35 # fits most messages nicely
"""Default text area size for boxed messages"""

MAX_BOX_SIZE = 100
"""Maximum text area size for boxed messages"""

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


OTHER_CONT_CLASS = 'dim italic'  # grey for all containment classes
"""rich style used for containment classes not in CONT_CLASS_COLOURS"""

CONT_CLASS_COLOURS = defaultdict(
    lambda: OTHER_CONT_CLASS,
    {
        'Safe': CLEAR_LVL_COLOURS[1],
        'Euclid': CLEAR_LVL_COLOURS[3],
        'Keter': CLEAR_LVL_COLOURS[5],
    }
)
"""
Styles used in containment class & secondary class rendering

keys are containment classes
(eg, CONT_CLASS_COLOURS['Safe'] is used for Safe class)
"""


# === Other Constants ===

PLACEHOLDER = '\x00\x00'
"""Placeholder string for escaped colons in text formatting"""

SPECIAL_TEXTS = ['[DATA EXPUNGED]', 'None', 'Inactive']
"""Texts styled with OTHER_CONT_CLASS"""

ACTIVE_TEXT = 'Active'
"""Text styled in green"""


# === Regex Patterns ===

DIGIT_REGEX = r'(?<!O)5|[0-46-9]'
"""Regex pattern matching digits, excluding O5"""

QUOTED_REGEX = r'"[^"]*"'
"""Regex pattern matching text in double quotes"""


# === system.py constants ===

LOAD_RATE = 2
"""`lambd` value to use for `random.expovariate`"""

HICCUP_PROBABILITY = 0.25
"""Probability `sim_load` should encounter a hiccup"""

HICCUP_DELAY = (1, 2.5)
"""Args for `random.uniform` when a hiccup is encountered"""

SPECIAL_TITLES = ['O5 Council Member', 'Site Director', 'Administrator']
"""User titles that get a fancy login screen"""

AUTH_TYPES = {
     'O5 Council Member': 'O5',
     'Site Director': 'DIRECTOR',
     'Administrator': 'ADMINISTRATOR'
}
"""Authorization types associated with each special title"""
