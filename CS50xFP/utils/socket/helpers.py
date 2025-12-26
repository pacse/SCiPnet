"""
Helpers for socket operations
"""

from json import dumps, loads, JSONDecodeError
import socket
from struct import pack
from typing import Any, Generator
from contextlib import contextmanager

from ..general.server_config import Socket as SockConf
from ..general.validation import validate_data, validate_conn, validate_field
from ..general.exceptions import MaxSizeLimitError



# === Type Aliases ===

ExceptionTypes = type[Exception] | tuple[type[Exception], ...]



# === Main Functions ===

def gen_socket_conn() -> socket.socket:
    """
    Generates a socket connection with:
    - AF_INET as address family
    - SOCK_STREAM as socket type

    Returns
    -------
    socket.socket
        A socket connection
    """
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.settimeout(SockConf.DEF_TIMEOUT)
    return conn


def encode(data: Any) -> bytes:
    """
    Encodes `data` as bytes

    Parameters
    ----------
    data : Any
        The data to encode

    Returns
    -------
    bytes
        The encoded data in the format:
        [4 bytes size][JSON encoded data]

    Raises
    ------
    ValueError
        If `data` is None or empty
    MaxSizeLimitError
        If the encoded data size exceeds maximum allowed size
    """
    validate_data(data)

    encoded_data = dumps(data).encode()
    size = pack(SockConf.S_TYPE, len(encoded_data))
    result = size + encoded_data

    if len(result) > SockConf.MAX_MSG_S:
        raise MaxSizeLimitError(len(result), SockConf.MAX_MSG_S)
    return result

def decode(data: bytes) -> Any:
    """
    Decodes `data` from bytes to original format

    Parameters
    ----------
    data : bytes
        The data to decode

    Returns
    -------
    Any
        The decoded data
    """
    validate_field('data', data, bytes)

    try:
        return loads(data.decode())
    except (UnicodeDecodeError, JSONDecodeError) as e:
        raise ValueError(f'Error decoding data: {e}') from e

@contextmanager
def socket_context_manager(
                           message: str,
                           conn: socket.socket,
                           short_timeout: bool = False,
                           reraise: ExceptionTypes = ConnectionError
                          ) -> Generator[None, None, None]:
    """
    Context manager to simplify socket operations:
    - Validates `conn`
    - Sets short timeout if `short_timeout` is True

    - Reraises exceptions in `reraise`
    - Raises other exceptions under `ConnectionError`

    - Resets timeout on exit if `short_timeout` is True

    Parameters
    ----------
    message : str
        The message to include in ConnectionError
    conn : socket.socket
        The socket connection (for validation)
    short_timeout : bool
        Whether to shorten the timeout during the context
    reraise : type[Exception] | tuple[type[Exception], ...] = ConnectionError
        The exception(s) to reraise

    Yields
    ------
    None

    Raises
    ------
    TypeError
        If `conn` is not a socket.socket instance
    ConnectionError
        If an exception not in `reraise` occurs: f'{message}: {e}'
    """
    validate_conn(conn)

    if short_timeout:
        conn.settimeout(SockConf.TMP_TIMEOUT)

    try:
        yield

    except reraise:
        raise
    except Exception as e:
        raise ConnectionError(f'{message}: {e}') from e

    finally:
        if short_timeout:
            conn.settimeout(SockConf.DEF_TIMEOUT)


def test_send(conn: socket.socket) -> None:
    """
    Tests `conn` by sending test data

    Parameters
    ----------
    conn : socket.socket
        The socket connection to test

    Raises
    ------
    TypeError
        If `conn` is not a socket.socket instance
    ConnectionError
        If the connection test fails
    """

    with socket_context_manager(
        'Connection test failed', conn, True
    ):
        conn.sendall(SockConf.TEST_MSG)
        result = conn.recv(SockConf.TEST_S)

        if result != SockConf.ACK_MSG:
            raise ConnectionError(
                f'Did not receive ACK: got {result!r}'
                f', expected {SockConf.ACK_MSG!r}'
            )

def test_recv(conn: socket.socket) -> None:
    """
    Tests `conn` by receiving test data

    Parameters
    ----------
    conn : socket.socket
        The socket connection to test

    Raises
    ------
    TypeError
        If `conn` is not a socket.socket instance
    ConnectionError
        If the connection test fails
    """

    with socket_context_manager(
        'Connection test failed', conn, True
    ):
        result = conn.recv(SockConf.TEST_S)

        if result != SockConf.TEST_MSG:
            raise ConnectionError(
                f'Did not receive TEST_MSG: got {result!r}'
                f', expected {SockConf.TEST_MSG!r}'
            )

        conn.sendall(SockConf.ACK_MSG)



# === Exports ===

__all__ = [
           'gen_socket_conn',
           'test_send',
           'test_recv'
          ]
