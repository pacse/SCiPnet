"""
Display functions related to file access

- redacted()
- expunged()
- granted()
"""

from .core.boxes import basic_box_with_text

def redacted(file: str, file_classification: str, usr_clearance: str) -> None:
    """
    prints a message saying `file` is above your clearance

    art by ChatGPT
    """

    basic_box_with_text(
        [
         f'FILE_REF: {file} REDACTED',
         f'CLEARANCE {file_classification} REQUIRED',
         f'(YOU ARE CLEARANCE {usr_clearance})'
        ],
        ['ACCESS DENIED'],

    )


def expunged(file: str) -> None:
    """
    prints a message saying `file` has been expunged

    art by ChatGPT
    """

    basic_box_with_text(
        [f'FILE_REF: {file} NOT FOUND'],
        ['DATA EXPUNGED'],
    )


def granted(file: str) -> None:
    """
    prints a message saying access has been granted to `file`

    art by ChatGPT
    """

    basic_box_with_text(
        [f'FILE_REF: {file} ACCESS GRANTED'],
        ['ACCESS GRANTED'],
    )
