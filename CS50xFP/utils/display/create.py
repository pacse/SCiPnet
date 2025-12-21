"""
Display functions related to file creation
"""

from .core.boxes import basic_box_with_text
from ..general.display_config import CreateMessages as CM
from .helpers import check_type_and_empty_str



def create_f(f_type: str) -> None:
    """
    Prints a simple message for file creation

    Parameters
    ----------
    f_type : str
        the type of file being created

    Raises
    ------
    TypeError
        If `f_type` is not a string
    ValueError
        If `f_type` is empty or whitespace

    Notes
    -----
    - Calls `basic_box_with_text()` with `RAISA_log = True`
    - Art by ChatGPT
    """

    check_type_and_empty_str(f_type, 'f_type')

    basic_box_with_text(
                        [CM.CREATE_BOX],
                        [f_type.upper()]
                       )


def clearance_denied(
                     required_clearance: str,
                     user_clearance: str
                    ) -> None:
    """
    Tells the usr they have insufficient clearance for file creation

    Parameters
    ----------
    required_clearance : str
        the clearance level needed to create the file
    user_clearance : str
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

    check_type_and_empty_str(required_clearance, 'required_clearance')
    check_type_and_empty_str(user_clearance, 'user_clearance')


    basic_box_with_text(
                        [CM.INSUFFICIENT_CLEAR_BOX],
                        [
                         CM.CLEAR_REQUIRED.format(
                            needed_clear=required_clearance
                         ),
                         CM.USER_CLEAR.format(usr_clear=user_clearance)
                        ]
                       )


def invalid_f_type(f_type: str) -> None:
    """
    Tells a user `f_type` is not a valid filetype

    Parameters
    ----------
    f_type : str
        the file type being created

    Raises
    ------
    TypeError
        If `f_type` is not a string
    ValueError
        If `f_type` is empty or whitespace

    Notes
    -----
    - Calls `basic_box_with_text()` with `RAISA_log = True`
    """

    check_type_and_empty_str(f_type, 'f_type')

    basic_box_with_text(
                        [CM.INVALID_FD_BOX],
                        [CM.NOT_VALID.format(f_type=f_type)]
                       )


def invalid_f_data() -> None:
    """
    Tells a user file data is invalid
    """
    basic_box_with_text(
                        [CM.INVALID_FD_BOX],
                        [CM.CHECK_DATA, CM.PERSISTS]
                       )


def no_data_recvd() -> None:
    """
    Tells a user the server received no data

    Notes
    -----
    - Calls `basic_box_with_text()` with `RAISA_log = True`
    - Art by ChatGPT
    """
    basic_box_with_text(
                        [CM.NO_DATA_RECVD_BOX],
                        [*CM.TRY_AGAIN]
                       )


def no_response() -> None:
    """
    Tells usr that no response was received from the server

    art by ChatGPT, formatting by me
    """
    basic_box_with_text(
                        [CM.NO_RESPONSE_BOX],
                        [*CM.TRY_AGAIN]
                       )


def created_f(f_type: str, f_id: int) -> None:
    """
    Prints a message saying a file was successfully created

    Parameters
    ----------
    f_type : str
        the type of file being created
    f_id : int
        the ID of the created file

    Raises
    ------
    TypeError
        - If `f_type` is not a string
        - If `f_id` is not an int
    ValueError
        - If `f_type` is empty or whitespace
        - If `f_id` is negative

    Notes
    -----
    - Calls `basic_box_with_text()` with `RAISA_log = True`
    - Art by ChatGPT
    """

    check_type_and_empty_str(f_type, 'f_type')

    if not isinstance(f_id, int):
        raise TypeError('f_id must be an int')
    if f_id < 0:
        raise ValueError('f_id must be positive')

    basic_box_with_text(
                        [CM.FILE_CREATED_BOX],
                        [
                         CM.FILE_CREATED.format(
                            file_ref=f'{f_type.upper()}-{f_id:03d}'
                         )
                        ]
                       )
