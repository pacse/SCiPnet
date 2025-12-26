"""
Message formats for socket communication

Contains
--------
- MESSAGE_KEYS
- MessageTypes

- Message
- MessageData
- Messages
- MessageDatas

- format_map
"""

from typing import Any, TypedDict, Literal
from enum import StrEnum

# === Message Formats ===

MESSAGE_KEYS = {'type', 'data'}
"""All keys present in every message TypedDict"""


class MessageTypes(StrEnum):
    """
    All message type Literals

    Contains
    --------
    - AUTH_REQUEST
    - AUTH_FAILED
    - AUTH_SUCCESS

    - ACCESS_REQUEST
    - ACCESS_REDACTED
    - ACCESS_EXPUNGED
    - ACCESS_GRANTED
    """
    AUTH_REQUEST = 'auth_request'
    AUTH_FAILED = 'auth_failed'
    AUTH_SUCCESS = 'auth_success'

    ACCESS_REQUEST = 'access_request'
    ACCESS_REDACTED = 'access_redacted'
    ACCESS_EXPUNGED = 'access_expunged'
    ACCESS_GRANTED = 'access_granted'



# === Data Formats ===

class AuthRequestData(TypedDict):
    """
    Data for authentication request from client

    Parameters
    ----------
    user_id : int
        The entered user ID
    password : str
        The entered password
    """
    user_id: int
    password: str

class AuthFailedData(TypedDict):
    """
    Data for authentication failure response from server

    Parameters
    ----------
    field : str
        The field that caused the failure (eg. 'user_id' if user not found)
    """
    field: str

class AuthSuccessData(TypedDict):
    """
    Data for authentication success response from server

    Parameters
    ----------
    user : dict[str, Any]
        The dumped Pydantic User model
    """
    user: dict[str, Any]


class AccessRequestData(TypedDict):
    """
    Data for access request from client

    Parameters
    ----------
    f_type : str
        The type of the file (eg. 'SCP', 'MTF', etc.)
    f_id : int
        The ID of the file
    """
    f_type: str
    f_id: int

class AccessRedactedData(TypedDict):
    """
    Data for access redacted response from server

    Parameters
    ----------
    user_clear : str
        The user's clearance level (eg. 'Level 3 - Confidential')
    user_hex : str
        The colour to render the user's clearance level with
    needed_clear : str
        The needed clearance level for the file
    needed_hex : str
        The colour to render the needed clearance level with
    """
    user_clear: str
    user_hex: str
    needed_clear: str
    needed_hex: str

class AccessExpungedData(TypedDict):
    """
    Data for access expunged response from server

    Parameters
    ----------
    f_type : str
        The type of the file
    f_id : int
        The ID of the file
    """
    f_type: str
    f_id: int

class AccessGrantedData(TypedDict):
    """
    Data for access granted response from server

    Parameters
    ----------
    file : dict[str, Any]
        The dumped file data
    """
    file: dict[str, Any]



# === Message Types ===

class AuthRequest(TypedDict):
    type: Literal[MessageTypes.AUTH_REQUEST]
    data: AuthRequestData

class AuthFailed(TypedDict):
    type: Literal[MessageTypes.AUTH_FAILED]
    data: AuthFailedData

class AuthSuccess(TypedDict):
    type: Literal[MessageTypes.AUTH_SUCCESS]
    data: AuthSuccessData


class AccessRequest(TypedDict):
    type: Literal[MessageTypes.ACCESS_REQUEST]
    data: AccessRequestData

class AccessRedacted(TypedDict):
    type: Literal[MessageTypes.ACCESS_REDACTED]
    data: AccessRedactedData

class AccessExpunged(TypedDict):
    type: Literal[MessageTypes.ACCESS_EXPUNGED]
    data: AccessExpungedData

class AccessGranted(TypedDict):
    type: Literal[MessageTypes.ACCESS_GRANTED]
    data: AccessGrantedData



AuthMessages = AuthRequest | AuthFailed | AuthSuccess
AuthDatas = AuthRequestData | AuthFailedData | AuthSuccessData

AccessMessages = (
    AccessRequest | AccessRedacted | AccessExpunged | AccessGranted
)
AccessDatas = (
    AccessRequestData | AccessRedactedData |
    AccessExpungedData | AccessGrantedData
)

Message = AuthMessages | AccessMessages
"""Generic Message TypedDict"""

MessageData = AuthDatas | AccessDatas
"""Generic Message Data TypedDict"""


format_map = {
    MessageTypes.AUTH_REQUEST: AuthRequestData,
    MessageTypes.AUTH_FAILED: AuthFailedData,
    MessageTypes.AUTH_SUCCESS: AuthSuccessData,
    MessageTypes.ACCESS_REQUEST: AccessRequestData,
    MessageTypes.ACCESS_REDACTED: AccessRedactedData,
    MessageTypes.ACCESS_EXPUNGED: AccessExpungedData,
    MessageTypes.ACCESS_GRANTED: AccessGrantedData
}
"""Maps MessageTypes to their respective Data TypedDicts"""


# === Exports ===

class Messages:
    """
    All message TypedDicts

    Contains
    --------
    - AuthRequest
    - AuthFailed
    - AuthSuccess

    - AccessRequest
    - AccessRedacted
    - AccessExpunged
    - AccessGranted
    """
    AuthRequest = AuthRequest
    AuthFailed = AuthFailed
    AuthSuccess = AuthSuccess

    AccessRequest = AccessRequest
    AccessRedacted = AccessRedacted
    AccessExpunged = AccessExpunged
    AccessGranted = AccessGranted

class MessageDatas:
    """
    All message data TypedDicts

    Contains
    --------
    - AuthRequestData
    - AuthFailedData
    - AuthSuccessData

    - AccessRequestData
    - AccessRedactedData
    - AccessExpungedData
    - AccessGrantedData
    """
    AuthRequestData = AuthRequestData
    AuthFailedData = AuthFailedData
    AuthSuccessData = AuthSuccessData

    AccessRequestData = AccessRequestData
    AccessRedactedData = AccessRedactedData
    AccessExpungedData = AccessExpungedData
    AccessGrantedData = AccessGrantedData


__all__ = [
           'MESSAGE_KEYS',
           'MessageTypes',

           'Message',
           'MessageData',
           'Messages',
           'MessageDatas',

           'format_map',
          ]
