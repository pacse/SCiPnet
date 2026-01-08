"""
Socket utilities for client and server communication
"""

# TODO: Implement TLS: after submit final project
from struct import unpack
from typing import Any, cast, Mapping
import socket

from .helpers import encode, decode, socket_context_manager
from .builders import gen_msg
from .protocol import MessageTypes, Message, MessageData
from ..general.server_config import Socket as SockConf
from ..general.exceptions import MaxSizeLimitError
from ..general.validation import validate_msg


# === Main Funcs ===

# TODO: Add overloads similar to builders.py (after submit final project)
def send(
         conn: socket.socket,
         msg_type: MessageTypes,
         msg_data: Mapping[str, Any]
        ) -> None:
    """
    Builds a Message from `msg_type` and `msg_data` and sends it over `conn`

    Parameters
    ----------
    conn : socket.socket
        The socket connection to send data over
    msg_type : MessageTypes
        The message type
    msg_data : Mapping[str, Any]
        The message data

    Raises
    ------
    TypeError
        If `conn` is not a socket.socket instance
    ValueError
        If `data` is None or empty
    ConnectionError
        If there is an error transmitting data
    """

    # build data
    data = encode(gen_msg(msg_type, cast(MessageData, msg_data)))

    with socket_context_manager(
        'Error sending data', conn,
    ):
        conn.sendall(data)


def recv(conn: socket.socket) -> Message:
    """
    Receives and returns a Message from `conn`

    Parameters
    ----------
    conn : socket.socket
        The socket connection to receive data from

    Returns
    -------
    Message
        The received message

    Raises
    ------
    TypeError
        If `conn` is not a socket.socket instance
    ConnectionError
        If there is an error receiving data:
        - Connection lost
        - Incomplete size header
        - Message size exceeds maximum allowed size
    MaxSizeLimitError
        If the received message size exceeds maximum allowed size
    """

    with socket_context_manager(
        'Error receiving data', conn,
        reraise=(MaxSizeLimitError, ConnectionError, ConnectionAbortedError)
    ):
        # get size header
        header = conn.recv(SockConf.HEADER_S)

        if not header or len(header) != SockConf.HEADER_S:
            raise ConnectionError(
                f'Connection lost or received incomplete size header: {header!r}'
            )

        msg_size = unpack(SockConf.S_TYPE, header)[0]

        # validate
        if msg_size > SockConf.MAX_MSG_S:
            raise MaxSizeLimitError(msg_size, SockConf.MAX_MSG_S, False)

        # prevent infinite loop when receiving
        max_chunks = msg_size // SockConf.RCV_S + 1
        chunk_count = 0

        # receive exactly `msg_size` bytes
        data = b''

        while len(data) < msg_size:
            if chunk_count > max_chunks:
                raise ConnectionError('Exceeded expected message chunks')

            remaining = msg_size - len(data)
            buff = conn.recv(min(SockConf.RCV_S, remaining))

            if not buff: # check buffer
                raise ConnectionAbortedError(
                    'Connection lost during data reception'
                )

            data += buff
            chunk_count += 1

    # decode, validate, & return
    decoded = decode(data)
    return validate_msg(decoded, Message) # type: ignore[arg-type] (bad, but works)


# === Exports ===

__all__ = [
           'send',
           'recv',
          ]
