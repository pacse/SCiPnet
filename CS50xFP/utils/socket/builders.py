"""
Message builders for socket communication

Contains
--------
- gen_msg
- gen_auth_request
- gen_auth_failed
- gen_auth_success

- gen_access_request
- gen_access_redacted
- gen_access_expunged
- gen_access_granted
"""
from typing import Any, overload, Literal, cast

from .protocol import (
    MessageTypes, Messages, MessageDatas, Message, MessageData, format_map
)

from ..general.validation import validate_hex, validate_dict, validate_str, \
                                 validate_int, validate_enum
from ..general.exceptions import arg_error, field_error
from ..sql.transformers import Models as PyModels, PydanticBase
from ..general.server_config import Server as ServerCfg




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
              msg_type: Literal[MessageTypes.ACCESS_TYPE_FAIL],
              data: MessageDatas.AccessTypeFailData
             ) -> Messages.AccessTypeFail: ...

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
            data: dict[str, str]
           ) -> Messages.AccessGranted: ...

@overload
def gen_msg(
            msg_type: MessageTypes,
            data: MessageData
           ) -> Message: ...

def gen_msg(
            msg_type: str | MessageTypes,
            data: dict[str, Any] | MessageData
           ) -> Message:
    """
    Generates a generic message

    Parameters
    ----------
    msg_type : str | MessageTypes
        The message type (string or enum member)
    data : dict[str, Any] | MessageData
        The message data

    Returns
    -------
    Message
        The generated message

    Raises
    ------
    TypeError
        - If `msg_type` is not a member of MessageTypes
        - If `data` is not a dict with str keys
        - If `data` does not match the expected format for `msg_type`
    """

    validated_type = validate_enum('msg_type', msg_type, MessageTypes)
    expected_format = format_map.get(validated_type)
    if expected_format:
        validate_dict('data', data, expected_format)
    else:
        raise field_error(
            'msg_type', msg_type,
            f"msg_type to have a corresponding 'data' TypedDict"
        )

    return cast(Message, {
        'type': msg_type,
        'data': data
    })



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

def gen_access_type_fail(
                         tried: str
                        ) -> Messages.AccessTypeFail:
    """
    Generates an AccessTypeFail message

    Parameters
    ----------
    tried : str
        The invalid file type that was tried

    Returns
    -------
    AccessTypeFail : dict[str, Any]
        The generated AccessTypeFail message
    """
    validate_str('tried', tried)

    return gen_msg(
        MessageTypes.ACCESS_TYPE_FAIL,
        {
         'tried': tried,
         'valid': [k for k in ServerCfg.VALID_F_TYPES.keys()]
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
                       data: dict[str, str]
                      ) -> Messages.AccessGranted:
    """
    Generates an AccessGranted message

    Parameters
    ----------
    data : dict[str, str]
        The gathered file data

    Returns
    -------
    AccessGranted : dict[str, Any]
        The generated AccessGranted message
    """
    validate_dict('data', data)

    return gen_msg(
        MessageTypes.ACCESS_GRANTED,
        data
    )
