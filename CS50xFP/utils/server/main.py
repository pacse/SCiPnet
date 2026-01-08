"""
Main server instance (Run this to start the server)

Contains
--------
- handle_usr(client: socket.socket, c_ip: str, t_id: int) -> None
"""

import socket
from threading import active_count, Thread
from itertools import count

from .actions import access
from .basic import auth_usr
from ..socket import send, recv, MessageTypes, gen_socket_conn
from ..socket.protocol import AuthRequest, AccessRequest
from ..general.validation import validate_msg


def handle_usr(
               client: socket.socket,
               c_ip: str,
               t_id: int
              ) -> None:
    """
    Handles a user connection (run on server threads)

    Parameters
    ----------
    client : socket.socket
        the client socket
    c_ip : str
        the client's ip address
    t_id : int
        the thread id
    """

    try:

        # === Authenticate user ===

        auth_msg = validate_msg(recv(client), AuthRequest)

        invalid_field, usr = auth_usr(
            auth_msg['data']['user_id'], auth_msg['data']['password']
        )

        # auth failed (or not usr to make type checker happy)
        if invalid_field or not usr:
            send(
                client, MessageTypes.AUTH_FAILED,
                {'field': invalid_field}
            )
            print(f'[THREAD {t_id}] Authentication failed for {c_ip}')
            return


        # auth success
        send(
            client, MessageTypes.AUTH_SUCCESS,
            {'user': usr.model_dump_json()}
        )
        print(f'[THREAD {t_id}] Authentication successful for {c_ip}')


        # Handle access requests
        while True:

            # get access request
            try:
                access_msg = validate_msg(recv(client), AccessRequest)
            except ConnectionAbortedError:
                print(f'[THREAD {t_id}] Connection closed by {c_ip}')
                break

            # process
            access_response = access(
                access_msg['data']['f_type'],
                access_msg['data']['f_id'],
                usr,
                c_ip
            )

            # respond
            send(
                client, access_response['type'],
                access_response['data']
            )

    # ensure conn is always closed
    finally:
        print(f'[THREAD {t_id}] Closing connection to {c_ip}')
        client.close()
        print(
              f'[THREAD {t_id}] Done | Active '
              f'connections: {active_count() - 2}'
             )



if __name__ == '__main__':
    """Starts the server and listens for connections"""
    thread_counter = count(1)

    with gen_socket_conn(bind=True) as server:
        print('[Server] Waiting for a connection . . .')
        server.listen()

        while True:
            try:
                conn, addr = server.accept()

                ip = addr[0]  # conn ip

                print(
                      f'[Server] Connection from {ip} | '
                      f'Thread ID: {active_count() - 1}'
                     )

                Thread(
                       target=handle_usr,
                       args=(conn, ip, next(thread_counter))
                      ).start()

                print(f'[Server] Active connections: {active_count() - 1}')
            except KeyboardInterrupt:
                print('[Server] Exiting')
                break


__all__ = ['handle_usr']
