"""
Display functions related to file access

- redacted()
- expunged()
- granted()
"""

from .core.boxes import basic_box_with_text
from .config import AccessMessages as AM
from .helpers import check_type_and_empty_str


def redacted(
             file_ref: str,
             file_classification: str,
             usr_clearance: str
            ) -> None:
    """
    prints a message saying `file_ref` is above your clearance

    Parameters
    ----------
    file_ref : str
        the file reference being accessed
    file_classification : str
        the classification level of the file
    usr_clearance : str
        the clearance level of the user

    Raises
    ------
    TypeError
        If any parameter is not a string
    ValueError
        If any parameter is empty or whitespace

    Notes
    -----
    - Calls `basic_box_with_text()` with `RAISA_log = True`
    - Art by ChatGPT
    """

    # validation
    for v, v_name in [
                      (file_ref, 'file_ref'),
                      (file_classification, 'file_classification'),
                      (usr_clearance, 'usr_clearance')
                     ]:
        check_type_and_empty_str(v, v_name)

    basic_box_with_text(
                        [AM.REDACTED_BOX],
                        [
                         AM.REDACTED_FILE.format(file_ref=file_ref),
                         AM.REDACTED_REQUIRED.format(
                            file_clear=file_classification
                         ),
                         AM.REDACTED_USER.format(usr_clear=usr_clearance)
                        ]
                       )


def expunged(file_ref: str) -> None:
    """
    prints a message saying `file_ref` has been expunged

    Parameters
    ----------
    file_ref : str
        the file reference being accessed

    Raises
    ------
    TypeError
        If `file_ref` is not a string
    ValueError
        If `file_ref` is empty or whitespace

    Notes
    -----
    - Calls `basic_box_with_text()` with `RAISA_log = True`
    - Art by ChatGPT
    """

    check_type_and_empty_str(file_ref, 'file_ref')

    basic_box_with_text(
                        [AM.EXPUNGED_BOX],
                        [AM.EXPUNGED_FILE.format(file_ref=file_ref)],
                       )


def granted(file_ref: str) -> None:
    """
    prints a message saying access has been granted to `file_ref`

    Parameters
    ----------
    file_ref : str
        the file reference being accessed

    Raises
    ------
    TypeError
        If `file_ref` is not a string
    ValueError
        If `file_ref` is empty or whitespace

    Notes
    -----
    - Calls `basic_box_with_text()` with `RAISA_log = True`
    - Art by ChatGPT
    """

    check_type_and_empty_str(file_ref, 'file_ref')

    basic_box_with_text(
                        [AM.GRANTED_BOX],
                        [AM.GRANTED_FILE.format(file_ref=file_ref)],
                       )
