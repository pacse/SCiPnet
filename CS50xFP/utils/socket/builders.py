"""
Message builders for socket communication

Contains
--------
- gen_auth_request
- gen_auth_failed
- gen_auth_success

- gen_access_request
- gen_access_redacted
- gen_access_expunged
- gen_access_granted
"""
from typing import Any, overload, Literal

from .protocol import (
    MessageTypes, format_map, Messages, MessageDatas, Message
)

from ..general.validation import validate_hex, validate_dict, validate_str, \
                                 validate_int, validate_enum, validate_msg
from ..general.exceptions import arg_error
from ..sql.transformers import Models as PyModels, PydanticBase




# === Main Generator Func ===

@overload
def gen_msg(
              msg_type: Literal[MessageTypes.AUTH_REQUEST],
              data: MessageDatas.AuthRequestData
             ) -> Messages.AuthRequest: ...

@overload
def gen_msg(
              msg_type: Literal[MessageTypes.AUTH_FAILED],
              data: MessageDatas.AuthFailedData
             ) -> Messages.AuthFailed: ...

@overload
def gen_msg(
              msg_type: Literal[MessageTypes.AUTH_SUCCESS],
              data: MessageDatas.AuthSuccessData
             ) -> Messages.AuthSuccess: ...

@overload
def gen_msg(
              msg_type: Literal[MessageTypes.ACCESS_REQUEST],
              data: MessageDatas.AccessRequestData
             ) -> Messages.AccessRequest: ...

@overload
def gen_msg(
              msg_type: Literal[MessageTypes.ACCESS_REDACTED],
              data: MessageDatas.AccessRedactedData
             ) -> Messages.AccessRedacted: ...

@overload
def gen_msg(
              msg_type: Literal[MessageTypes.ACCESS_EXPUNGED],
              data: MessageDatas.AccessExpungedData
             ) -> Messages.AccessExpunged: ...

@overload
def gen_msg(
              msg_type: Literal[MessageTypes.ACCESS_GRANTED],
              data: MessageDatas.AccessGrantedData
             ) -> Messages.AccessGranted: ...

def gen_msg(
              msg_type: str | MessageTypes,
              data: dict[str, Any]
             ) -> Message:
    """
    Generates a generic message

    Parameters
    ----------
    msg_type : str | MessageTypes
        The message type (string or enum member)
    data : dict[str, Any]
        The message data

    Returns
    -------
    Message
        The generated message

    Raises
    ------
    TypeError
        - If `msg_type` is not a member of MessageTypes
        - If `data` is not a dict
        - If `data` does not match the expected format for `msg_type`
    """
    msg_type = validate_enum('msg_type', msg_type, MessageTypes)
    data = validate_msg(data)

    return {
        'type': msg_type.value,
        'data': data
    }



# === Generator Implementations ===

def gen_auth_request(
                     user_id: int,
                     password: str
                    ) -> Messages.AuthRequest:
    """
    Generates an AuthRequest message

    Parameters
    ----------
    user_id : int
        The user ID
    password : str
        The password

    Returns
    -------
    AuthRequest : dict[str, Any]
        The generated AuthRequest message
    """
    validate_int('user_id', user_id)
    validate_str('password', password)

    return gen_msg(
        MessageTypes.AUTH_REQUEST,
        {
         'user_id': user_id,
         'password': password
        }
    )

def gen_auth_failed(
                    field: str
                   ) -> Messages.AuthFailed:
    """
    Generates an AuthFailed message

    Parameters
    ----------
    field : str
        The field that caused the failure (eg. 'user_id' if user not found)

    Returns
    -------
    AuthFailed : dict[str, Any]
        The generated AuthFailed message
    """
    validate_str('field', field)

    return gen_msg(
        MessageTypes.AUTH_FAILED,
        {
         'field': field
        }
    )

def gen_auth_success(
                      user: PyModels.User
                     ) -> Messages.AuthSuccess:
    """
    Generates an AuthSuccess message

    Parameters
    ----------
    user : Any
        The Pydantic User model

    Returns
    -------
    AuthSuccess : dict[str, Any]
        The generated AuthSuccess message
    """
    validate_dict('user', user.model_dump())

    return gen_msg(
        MessageTypes.AUTH_SUCCESS,
        {
         'user': user.model_dump()
        }
    )


def gen_access_request(
                      f_type: str,
                      f_id: int
                     ) -> Messages.AccessRequest:
    """
    Generates an AccessRequest message

    Parameters
    ----------
    f_type : str
        The file type (eg. 'User', 'SCP', etc.)
    f_id : int
        The file ID

    Returns
    -------
    AccessRequest : dict[str, Any]
        The generated AccessRequest message
    """
    validate_str('f_type', f_type)
    validate_int('f_id', f_id)

    return gen_msg(
        MessageTypes.ACCESS_REQUEST,
        {
         'f_type': f_type,
         'f_id': f_id
        }
    )

def gen_access_redacted(
                        user_clear: str,
                        user_hex: str,
                        needed_clear: str,
                        needed_hex: str
                       ) -> Messages.AccessRedacted:
    """
    Generates an AccessRedacted message

    Parameters
    ----------
    user_clear : str
        The user's clearance level (eg. 'Level 3 - Confidential')
    user_hex : str
        The colour to render `user_clear` with
    needed_clear : str
        The needed clearance level to access the file
    needed_hex : str
        The colour to render `needed_clear` with

    Returns
    -------
    AccessRedacted : dict[str, Any]
        The generated AccessRedacted message
    """
    validate_str('user_clear', user_clear)
    validate_hex('user_hex', user_hex)
    validate_str('needed_clear', needed_clear)
    validate_hex('needed_hex', needed_hex)

    return gen_msg(
        MessageTypes.ACCESS_REDACTED,
        {
         'user_clear': user_clear,
         'user_hex': user_hex,
         'needed_clear': needed_clear,
         'needed_hex': needed_hex
        }
    )

def gen_access_expunged(
                        f_type: str,
                        f_id: int
                       ) -> Messages.AccessExpunged:
    """
    Generates an AccessExpunged message

    Parameters
    ----------
    f_type : str
        The file type (eg. 'User', 'SCP', etc.)
    f_id : int
        The file ID

    Returns
    -------
    AccessExpunged : dict[str, Any]
        The generated AccessExpunged message
    """
    validate_str('f_type', f_type)
    validate_int('f_id', f_id)

    return gen_msg(
        MessageTypes.ACCESS_EXPUNGED,
        {
         'f_type': f_type,
         'f_id': f_id
        }
    )

def gen_access_granted(
                       file: PydanticBase
                      ) -> Messages.AccessGranted:
    """
    Generates an AccessGranted message

    Parameters
    ----------
    file : Any
        The Pydantic model of the file (eg. User, SCP, etc.)

    Returns
    -------
    AccessGranted : dict[str, Any]
        The generated AccessGranted message
    """
    if not hasattr(file, 'model_dump'):
        raise arg_error(
            'file', file,
            'File must be a Pydantic model instance'
        )

    return gen_msg(
        MessageTypes.ACCESS_GRANTED,
        {
         'file': file.model_dump()
        }
    )
