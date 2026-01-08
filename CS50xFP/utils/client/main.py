if __name__ == '__main__':
    from time import perf_counter as pc

    print('Initializing SCiPnet Terminal Session . . .')
    s = pc()


    import sys
    from rich.console import Console

    from .actions import access
    from ..socket import recv, send, gen_socket_conn, MessageTypes
    from ..socket.protocol import AuthMessages
    from ..display.system import startup, login, login_fail
    from ..display.create import no_response
    from ..display.access import invalid_response
    from ..display.helpers import clear, print_lines
    from ..general.validation import validate_msg
    from ..sql.transformers import User

    # enable/disable debug messages
    DEBUG = False

    # Quickstart for debugging (Messes up rich display sometimes ¯\_(ツ)_/¯)
    QS = True if len(sys.argv) == 3 else False

    with gen_socket_conn(connect=True) as server:
        print(f'Done. Took {pc()-s}s to initialise')

        if not QS:
            startup()
        console = Console()

        # === Authenticate ===

        user_id = int(sys.argv[1]) if QS else int(input('ID: '))
        password = sys.argv[2] if QS else input('Password: ')

        send(
            server, MessageTypes.AUTH_REQUEST,
            {'user_id': user_id, 'password': password}
        )
        result = validate_msg(recv(server), AuthMessages) # type: ignore[arg-type]

        if not result:
            no_response()
            sys.exit()

        if DEBUG:
            print(f'Result: {result}')

        if result['type'] == MessageTypes.AUTH_FAILED:
            login_fail(result['data']['field'])
            sys.exit()

        elif result['type'] == MessageTypes.AUTH_SUCCESS:
            usr = User.model_validate_json(result['data']['user'])
            login(usr)

        else:
            invalid_response()
            sys.exit()


        # === Main Loop ===
        while True:
            request = input('>>> ')
            split_request = request.upper().split()
            action = split_request[0]

            if action == 'ACCESS':
                if len(split_request) != 3:
                    print('Usage: ACCESS {filetype} {file_id}')
                    continue
                try:
                    f_type = split_request[1]
                    f_id = int(split_request[2])
                except ValueError:
                    print('file_id must be an integer')
                else:
                    access(server, console, f_type, f_id)

            elif action == 'LOGOUT':
                print('Logging out . . .')
                server.close()
                sys.exit()

            elif action in ['CLEAR', 'CLS']:
                clear()

            elif action == 'HELP':
                print_lines([
                    'Valid commands:',
                    'ACCESS {filetype} {file_id} - Accesses the specified deepwell entry',
                    'LOGOUT - Terminates the session',
                    'CLEAR (CLS) - Clears the terminal screen'
                ])

            else:
                print('INVALID COMMAND')
