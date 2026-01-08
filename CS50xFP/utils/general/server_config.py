"""
Configuration constants for server-side & socket logic

Contains
---
- Socket
- Server
"""

from struct import calcsize
from typing import Literal

from ..sql.schema import MainModels

# === Constants ===

class Socket:
    """
    Socket configuration constants

    Used In
    -------
    - socket.gen_socket_conn
    - socket.encode
    - socket.socket_context_manager
    - socket.test_send
    - socket.test_recv
    - socket.send
    - socket.recv

    Contains
    -------
    - DEF_TIMEOUT
    - TMP_TIMEOUT

    - HOST
    - PORT
    - ADDR

    - RCV_S
    - MAX_MSG_S

    - S_TYPE
    - HEADER_S

    - TEST_MSG
    - ACK_MSG
    - TEST_S
    """

    DEF_TIMEOUT = 60
    """Default socket timeout in seconds"""
    TMP_TIMEOUT = 2
    """Temporary socket timeout to use during tests in seconds"""

    HOST = '127.0.0.1'
    """Server IP address"""
    PORT = 65432
    """Server port"""
    ADDR = (HOST, PORT)
    """Server address tuple"""

    RCV_S = 1024 * 4
    """Receive buffer size in bytes (4 KB)"""
    MAX_MSG_S = (1024 ** 2) * 50
    """Maximum message size in bytes (50 MB)"""

    S_TYPE = '!I'
    """Size type for packing/unpacking message size with struct"""
    HEADER_S = calcsize(S_TYPE)
    """Header size in bytes (size of packed size type)"""

    TEST_MSG = b'\x01\x02\x03\x04'
    """Test message for connection verification"""
    ACK_MSG  = b'\x04\x03\x02\x01'
    """Acknowledgment message for connection verification"""
    TEST_S = len(TEST_MSG)
    """Size of test messages in bytes"""


class Server:
    """
    Server configuration constants

    Used In
    -------
    - TBC

    Contains
    -------
    - DEBUG
    - VALID_F_TYPES
    """

    DEBUG = False
    """Enable/disable debug messages"""

    VALID_F_TYPES: dict[
        Literal['SCP', 'MTF', 'SITE', 'USER'],
        type[MainModels.SCP] | type[MainModels.MTF] |
        type[MainModels.Site] | type[MainModels.User]
    ] = {
        'SCP': MainModels.SCP,
        "MTF": MainModels.MTF,
        "SITE": MainModels.Site,
        "USER": MainModels.User,
    }
    """
    Valid field types and their associated deepwell table model
    for various operations
    """



# === Exports ===

__all__ = ['Socket', 'Server']
