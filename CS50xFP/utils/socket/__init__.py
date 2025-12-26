"""
Socket communication utilities for server-client interaction
"""


from .transport import send, recv

from .builders import (
    gen_auth_request,
    gen_auth_failed,
    gen_auth_success,

    gen_access_request,
    gen_access_granted,
    gen_access_redacted,
    gen_access_expunged
)

from .protocol import (
    MessageTypes,
    MessageData, MessageDatas,
    Message, Messages
)

from .helpers import gen_socket_conn, test_send, test_recv


class Msg:
    """
    Message builders for socket communication

    Contains
    --------
    - auth_request
    - auth_failed
    - auth_success

    - access_request
    - access_redacted
    - access_expunged
    - access_granted
    """
    auth_request = staticmethod(gen_auth_request)
    auth_failed = staticmethod(gen_auth_failed)
    auth_success = staticmethod(gen_auth_success)

    access_request = staticmethod(gen_access_request)
    access_granted = staticmethod(gen_access_granted)
    access_redacted = staticmethod(gen_access_redacted)
    access_expunged = staticmethod(gen_access_expunged)

class Protocol:
    """
    Message types and data for socket communication

    Contains
    --------
    - Message
    - MessageData

    - MessageTypes
    - Messages
    - MessageDatas
    """
    Message = Message
    MessageData = MessageData


    MessageTypes = MessageTypes
    Messages = Messages
    MessageDatas = MessageDatas


__all__ = [
           'send',
           'recv',

           'Msg',
           'Protocol',

           'gen_socket_conn',
           'test_send',
           'test_recv',
          ]
