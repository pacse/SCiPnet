"""
Display configuration settings and constants

Contains
--------
- Boxes
- Styles
- Default_Formatting
- Formatting
- Bars
- General
- Load
- Login
"""

from collections import defaultdict
from dataclasses import dataclass

# disable markdown_it logging
# (causes problems with rich if not disabled)
import logging
logging.getLogger('markdown_it').setLevel(logging.WARNING)


# === Constants ===

class Boxes:
    """
    Box generator constants

    Used In
    -------
    - display.core.boxes.basic_box

    Contains
    --------
    - PADDING
    - DEF_TEXT_SIZE
    - MAX_TEXT_SIZE
    """

    PADDING = 4
    """
    Number of extra chars (left + right) to add to box width for padding
    """
    DEF_TEXT_SIZE = 35
    """Default text area size for boxed messages"""

    MAX_TEXT_SIZE = 100
    """Maximum text area size for boxed messages"""


class Styles:
    """
    Display styling constants

    Used In
    -------
    - display.core.bars.bars.acs_bar
    - display.core.bars.bars.user_bar
    - display.core.bars.lines.default_formatting
    - display.core.bars.template.BarTemplate._gen_classification_args

    Contains
    --------
    - CLEAR_LVL
    - OTHER_CONT_CLASS
    - CONT_CLASS
    """

    CLEAR_LVL = [
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

    OTHER_CONT_CLASS = 'dim italic'
    """rich style used for containment classes not in CONT_CLASS"""

    CONT_CLASS = defaultdict(
        lambda: Styles.OTHER_CONT_CLASS,
        {
            'Safe': CLEAR_LVL[1],
            'Euclid': CLEAR_LVL[3],
            'Keter': CLEAR_LVL[5],
        }
    )
    """
    Styles used in containment class & secondary class rendering

    keys are containment classes
    (eg, CONT_CLASS_COLOURS['Safe'] is used for Safe class)
    If a class is not in the keys, OTHER_CONT_CLASS is used
    """


class FormattingDefaults:
    """
    Default formatting constants

    Used In
    -------
    - display.core.bars.lines.default_formatting

    Contains
    --------
    - DIGIT_REGEX
    - DIGIT_STYLE
    - QUOTED_REGEX
    - QUOTED_STYLE

    - SPECIAL_TEXTS
    - ACTIVE_TEXT
    """


    DIGIT_REGEX = r'(?<!O)5|[0-46-9]'
    """Regex pattern matching digits, excluding O5"""
    DIGIT_STYLE = 'cyan bold'
    """rich style for digits"""

    QUOTED_REGEX = r'".+?"'
    """Regex pattern matching text in double quotes"""
    QUOTED_STYLE = 'green'
    """rich style for quoted text"""

    SPECIAL_TEXTS = ['[DATA EXPUNGED]', 'None', 'Inactive']
    """Texts styled with `Styles.OTHER_CONT_CLASS`"""

    ACTIVE_TEXT = 'Active'
    """Text styled in green"""

class Formatting:
    """
    Non-default formatting constants

    Used In
    -------
    - display.core.bars.lines._format_label_val_text

    Contains
    --------
    - PLACEHOLDER
    """

    PLACEHOLDER = '\x00\x00'
    """Placeholder string for escaped colons in text formatting"""


class Bars:
    """
    Constants for bar rendering

    Used In
    -------
    - display.core.bars.lines.format_centered_text
    - display.core.bars.lines.print_centered_line
    - display.core.bars.lines.print_piped_line
    - display.core.bars.template.BarTemplate.render_top_line

    Contains
    --------
    - TOP_SECTIONS
    - TEXT_WIDTH
    """

    TOP_SECTIONS = [32, 52, 32]
    """Width of text areas of the top bar (left, center, right)"""

    TEXT_WIDTH = 58
    """Width of text areas in 2-column bars"""


class Terminal:
    """
    General display constants for terminal rendering

    Used In
    -------
    - display.core.bars.bars
    - display.helpers.printc
    - display.system.sim_load
    - display.system.startup
    - display.helpers.printc
    - display.core.bars.lines.print_piped_line
    - display.core.bars.template.BarTemplate.__init__
    - display.core.bars.template.BarTemplate._render_sep
    - display.core.bars.template.BarTemplate.render_top_line


    Contains
    --------
    - MIN_TERM_WIDTH
    - SIZE
    - LEFT_PADDING
    """

    MIN_TERM_WIDTH = 120
    """
    Minimum terminal width required for proper display
    (largest fixed-width display is 120 chars)
    """

    @staticmethod
    def _validate_term_width(width: int) -> None:
        """validates terminal width is at least MIN_TERM_WIDTH"""
        if width < Terminal.MIN_TERM_WIDTH:
            raise RuntimeError(
                f'Terminal width too small for proper display: '
                f'got {width}, need at least {Terminal.MIN_TERM_WIDTH}'
            )

    @staticmethod
    def _get_term_width() -> int:
        """gets terminal width, adjusted to be even"""
        try:
            from os import get_terminal_size

            width = get_terminal_size().columns
            width = width - (width % 2) # make even

            Terminal._validate_term_width(width)
            return width

        except Exception as e:
            raise RuntimeError(f'Could not get terminal size:\n{e}') from e  # why must it be 1 space over 😭


    SIZE: int
    """Terminal width in columns, adjusted to be even"""

    LEFT_PADDING: str
    """Spaces to center 120 char content in terminal"""

# initialize SIZE and LEFT_PADDING
Terminal.SIZE = Terminal._get_term_width()
Terminal._validate_term_width(Terminal.SIZE)
Terminal.LEFT_PADDING = ' ' * ((Terminal.SIZE - Terminal.MIN_TERM_WIDTH) // 2)


class Load:
    """
    Loading simulation constants for `sim_load()`

    Used In
    -------
    - display.system.sim_load

    Contains
    --------
    - LOAD_RATE
    - HICCUP_PROBABILITY
    - HICCUP_DELAY
    - RAISA
    """

    LOAD_RATE = 2
    """`lambd` value to use for `random.expovariate`"""

    HICCUP_PROBABILITY = 0.25
    """Probability `sim_load` should encounter a hiccup"""

    HICCUP_DELAY = (1, 2.5)
    """Args for `random.uniform` when a hiccup is encountered"""

    RAISA = 'Recordkeeping And Information Security Administration'
    """Full name of RAISA"""


@dataclass(frozen=True)
class _LoginProfile:
    """Dataclass for login display profiles"""
    Auth_Type: str
    Clear_Type: str
    Welcome_Msg: str
    Logging_Msg: str
    Sys_Status_Msg: str

class Logins:
    """
    Profiles for login message display

    Used In
    -------
    - display.system._gen_login_lines
    - display.system.login

    Contains
    --------
    - PROFILES
    """

    _O5_COUNCIL_MEMBER = _LoginProfile(
            Auth_Type = 'O5',
            Clear_Type = '6 - COSMIC TOP SECRET',
            Welcome_Msg = 'Welcome back, {name}.',
            Logging_Msg = 'This session is being logged by CoreNode Zero.',
            Sys_Status_Msg = 'OPERATIONAL | DEEPWELL CHANNEL ENCRYPTED'
        )
    """Display profile for O5 Council Members"""

    _SITE_DIRECTOR = _LoginProfile(
            Auth_Type = 'DIRECTOR',
            Clear_Type = '5 - TOP SECRET',
            Welcome_Msg = 'Welcome back, {name}.',
            Logging_Msg = 'All actions are recorded and reviewed by O5 Liaison - Node Black',
            Sys_Status_Msg = 'OPERATIONAL | DEEPWELL CHANNEL ENCRYPTED'
        )
    """Display profile for Site Directors"""

    _ADMINISTRATOR = _LoginProfile(
            Auth_Type = 'ADMINISTRATOR',
            Clear_Type = 'UNBOUNDED | OVERRIDE: UNIVERSAL | LOGGING: DISABLED',
            Welcome_Msg = 'Welcome, Administrator. All systems stand by for your instruction.',
            Logging_Msg = 'There are no restrictions. There are no records.',
            Sys_Status_Msg = 'OPERATIONAL | DEEPWELL CHANNEL ENCRYPTED | ENCLAVE MODE ACTIVE'
        )
    """Display profile for The Administrator"""

    PROFILES: dict[str, _LoginProfile] = {
        'O5 Council Member': _O5_COUNCIL_MEMBER,
        'Site Director': _SITE_DIRECTOR,
        'Administrator': _ADMINISTRATOR
    }
    """Mapping of user titles to login display profiles"""

class FancyLogin:
    """
    Constants for fancy login box display

    Used In
    -------
    - display.system.login

    Contains
    --------
    - CONTENT_WIDTH
    - TB_LINE
    - L_R
    - SEP
    """
    _BORDER_WIDTH = 4 # left/right border width ('////')

    CONTENT_WIDTH = Terminal.MIN_TERM_WIDTH - _BORDER_WIDTH * 2
    """Width of text area inside fancy login box"""

    TB_LINE = '/' * Terminal.MIN_TERM_WIDTH
    """Top/bottom line for fancy login box"""

    L_R = '/' * _BORDER_WIDTH
    """Left/right border for fancy login box"""

    SEP = f'{L_R}{' ' * CONTENT_WIDTH}{L_R}'
    """Separator line for fancy login box"""


class AccessMessages:
    """
    Strings for access message display

    Used In
    -------
    - display.access.redacted
    - display.access.expunged
    - display.access.granted

    Contains
    --------
    - REDACTED_BOX
    - REDACTED_FILE
    - REDACTED_REQUIRED
    - REDACTED_USER

    - EXPUNGED_BOX
    - EXPUNGED_FILE

    - GRANTED_BOX
    - GRANTED_FILE
    """

    # redacted()
    REDACTED_BOX = 'ACCESS DENIED'
    """Box title for redacted access message"""
    REDACTED_FILE = 'FILE_REF: {file_type} {file_id} REDACTED'
    """File line for redacted access message"""
    REDACTED_REQUIRED = 'CLEARANCE {file_clear} REQUIRED'
    """Clearance level required line for redacted access message"""
    REDACTED_USER = '(YOU ARE CLEARANCE {usr_clear})'
    """User clearance level line for redacted access message"""

    # expunged()
    EXPUNGED_BOX = 'DATA EXPUNGED'
    """Box title for expunged access message"""
    EXPUNGED_FILE = 'FILE_REF: {file_type} {file_id} NOT FOUND'
    """File line for expunged access message"""

    # granted()
    GRANTED_BOX = 'ACCESS GRANTED'
    """Box title for granted access message"""
    GRANTED_FILE = 'FILE_REF: {file_type} {file_id} ACCESS GRANTED'
    """File line for granted access message"""

class CreateMessages:
    """
    Strings for file creation messages

    Used In
    -------
    - display.create.create_f
    - display.create.clearance_denied
    - display.create.invalid_f_type
    - display.create.invalid_f_data
    - display.create.no_data_recvd

    Contains
    --------
    - PERSISTS
    - TRY_AGAIN
    - FILE_CREATION_BOX
    - INSUFFICIENT_CLEARANCE_BOX
    - INVALID_FILE_TYPE_BOX
    - INVALID_FILE_DATA_BOX
    - NO_DATA_RECEIVED_BOX
    """

    PERSISTS = 'CONTACT YOUR SITE NETWORK ADMINISTRATOR IF ISSUES PERSIST'
    """Persistent issue message for file creation errors"""
    TRY_AGAIN = ['PLEASE TRY AGAIN', PERSISTS]
    """Basic try again message for file creation errors"""

    # create_f()
    CREATE_BOX = 'FILE CREATION'
    """Box title for file creation message"""

    # clearance_denied()
    INSUFFICIENT_CLEAR_BOX = 'INSUFFICIENT CLEARANCE'
    """Box title for insufficient clearance message"""
    CLEAR_REQUIRED = 'CLEARANCE {needed_clear} REQUIRED TO CREATE FILE'
    """Clearance level required line for insufficient clearance message"""
    USER_CLEAR = '(YOU ARE CLEARANCE {usr_clearance})'
    """User clearance level line for insufficient clearance message"""

    # invalid_f_type()
    INVALID_FILE_TYPE_BOX = 'INVALID FILE TYPE'
    """Box title for invalid file type message"""
    NOT_VALID = '{f_type} IS NOT A VALID FILE TYPE'
    """Invalid file type line for invalid file type message"""

    # invalid_f_data()
    INVALID_FD_BOX = 'INVALID FILE DATA'
    """Box title for invalid file data message"""
    CHECK_DATA = 'PLEASE CHECK FILE DATA AND TRY AGAIN'

    # no_data_recvd()
    NO_DATA_RECVD_BOX = 'NO DATA RECEIVED'
    """Box title for no data received message"""

    # created_f()
    FILE_CREATED_BOX = 'FILE CREATED SUCCESSFULLY'
    """Box title for file created message"""
    FILE_CREATED = 'FILE_REF: {file_ref} INITIALIZED'
    """File line for file created message"""


class GeneralMessages:
    # no_response()
    NO_RESPONSE_BOX = 'NO RESPONSE FROM DEEPWELL'
    """Box title for no response from deepwell message"""

    # invalid_response()
    INVALID_RESPONSE_BOX = 'INVALID RESPONSE FROM DEEPWELL'
    """Box title for invalid response message"""
