"""
Display functions related to file creation
"""
from .core.boxes import basic_box_with_text


from .config import CreateMessages as CM



def create_f(f_type: str) -> None:
    """
    Prints a simple message for file creation

    art by ChatGPT
    """
    basic_box_with_text(
                        [CM.CREATE_BOX],
                        [f_type.upper()]
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
    """
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

    Art by ChatGPT
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
    prints a message saying a file was successfully created

    art by ChatGPT
    """
    basic_box_with_text(
                        [CM.FILE_CREATED_BOX],
                        [
                         CM.FILE_CREATED.format(
                            file_ref=f'{f_type.upper()}-{f_id:03d}'
                         )
                        ]
                       )
