"""
Display functions related to file access

- redacted()
- expunged()
- granted()
"""

from .core.boxes import basic_box_with_text
from ..general.display_config import AccessMessages as AM, \
                                     GeneralMessages as GM, \
                                     CreateMessages as CM
from ..general.validation import validate_str


def redacted(
             file_type: str,
             file_id: int | str,
             file_classification: str,
             usr_clearance: str
            ) -> None:
    """
    Prints a message saying `file_type` `file_id` is above your clearance

    Parameters
    ----------
    file_type : str
        the type of the file being accessed
    file_id : int | str
        the ID of the file being accessed
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
                      (file_type, 'file_type'),
                      (str(file_id), 'file_id'),
                      (file_classification, 'file_classification'),
                      (usr_clearance, 'usr_clearance')
                     ]:
        validate_str(v_name, v)

    basic_box_with_text(
                        [AM.REDACTED_BOX],
                        [
                         AM.REDACTED_FILE.format(file_type=file_type, file_id=file_id),
                         AM.REDACTED_REQUIRED.format(
                            file_clear=file_classification
                         ),
                         AM.REDACTED_USER.format(usr_clear=usr_clearance)
                        ]
                       )


def expunged(file_type: str, file_id: int | str) -> None:
    """
    prints a message saying `file_type` `file_id` has been expunged

    Parameters
    ----------
    file_type : str
        the type of the file being accessed
    file_id : int | str
        the ID of the file being accessed

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

    validate_str('file_type', file_type)
    validate_str('file_id', str(file_id))

    basic_box_with_text(
                        [AM.EXPUNGED_BOX],
                        [AM.EXPUNGED_FILE.format(file_type=file_type, file_id=file_id)],
                       )


def granted(file_type: str, file_id: int | str) -> None:
    """
    prints a message saying access has been granted to `file_ref`

    Parameters
    ----------
    file_type : str
        the type of the file being accessed
    file_id : int | str
        the ID of the file being accessed

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
    validate_str('file_type', file_type)
    validate_str('file_id', str(file_id))

    basic_box_with_text(
                        [AM.GRANTED_BOX],
                        [AM.GRANTED_FILE.format(
                            file_type=file_type,
                            file_id=file_id)
                        ]
                       )


def invalid_response() -> None:
    """
    Tells a user that the server sent an invalid response


    Notes
    -----
    - Calls `basic_box_with_text()` with `RAISA_log = True`
    """

    basic_box_with_text(
                        [GM.INVALID_RESPONSE_BOX],
                        [*CM.TRY_AGAIN]
                       )
