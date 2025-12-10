"""
Display functions related to file creation
"""
from .core.boxes import basic_box_with_text


# reused a few times
PERSISTS = 'CONTACT YOUR SITE NETWORK ADMINISTRATOR IF ISSUES PERSIST'

TRY_AGAIN = [
    'PLEASE TRY AGAIN',
    PERSISTS
]


def create_f(f_type: str) -> None:
    """
    Prints a simple message for file creation

    art by ChatGPT
    """
    basic_box_with_text(
        ['FILE CREATION'],
        [f_type]
    )


def clearance_denied(
                     needed_clearance: str,
                     usr_clearance: str
                    ) -> None:
    """
    Tells the usr they have insufficient clearance for file creation

    art by ChatGPT
    """
    basic_box_with_text(
        ['INSUFFICIENT CLEARANCE'],
        [
         f'CLEARANCE {needed_clearance} REQUIRED TO CREATE FILE',
         f'(YOU ARE CLEARANCE {usr_clearance})'
        ]
    )


def invalid_f_type(f_type: str) -> None:
    """
    Tells a user `f_type` is not a valid filetype
    """
    basic_box_with_text(
        ['INVALID FILE TYPE'],
        [f'{f_type.upper()} IS NOT A VALID FILE TYPE'],
    )


def invalid_f_data() -> None:
    """
    Tells a user file data is invalid
    """
    basic_box_with_text(
        ['INVALID FILE DATA'],
        ['PLEASE CHECK FILE DATA AND TRY AGAIN', PERSISTS]
    )


def no_data_recvd() -> None:
    """
    Tells a user the server received no data

    Art by ChatGPT
    """
    basic_box_with_text(
        ['NO DATA RECEIVED BY SERVER'],
        TRY_AGAIN,
    )


def no_response() -> None:
    """
    Tells usr that no response was received from the server

    art by ChatGPT, formatting by me
    """
    basic_box_with_text(
        ['NO RESPONSE FROM DEEPWELL'],
        TRY_AGAIN,
    )


def created_f(f_type: str, f_id: int) -> None:
    """
    prints a message saying a file was successfully created

    art by ChatGPT
    """
    basic_box_with_text(
        ['FILE CREATED SUCCESSFULLY'],
        [f'{f_type.upper()}-{f_id:03d} INITIALIZED'],
    )
