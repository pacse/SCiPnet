'''
Client
'''
from time import perf_counter as pc

print("Initializing SCiPnet Terminal Session . . .")
start = pc()

import sys
from rich.console import Console

from utils import art
from CS50xFP.utils.sql.queries import User
from CS50xFP.utils.socket.transport import recv, send

from utils.basic import clear
import utils.client as client

# enable/disable debug messages
DEBUG = False

# Quickstart for debugging
QS = True if len(sys.argv) == 3 else False


if __name__ == "__main__":
    with client.conn_to_server() as server:
        print(f"Done. Took {pc()-start}s to initialise")
        if not QS:
            art.startup()  # print startup screen
        console = Console() # console to display markdown

        # authenticate
        id = sys.argv[1] if QS else int(input("ID: ")) # get ID
        password = sys.argv[2] if QS else input("Password: ") # get PW

        send(server, f"AUTH {id} {password}") # send auth request to server
        result = recv(server) # receive reply from server

        if not result: # no data, some error happened
            art.printc("[ERROR]: NO RESPONSE FROM DEEPWELL")
            server.close()
            sys.exit()

        if DEBUG: # debug flag
            print(f"Result: {result}")

        if result[0] == False: # invalid auth
            #TODO: prettify
            art.printc("INVALID AUTHORIZATION")
            art.printc("ACCESS DENIED")
            sys.exit()

        else: # valid auth
            usr = User(**result[1])
            art.login(usr)

        # main loop
        while True:
            request = input(">>> ") # get usr input
            split_request = request.upper().split()
            action = split_request[0]

            if action == "CREATE": # usr wants to create a file
                client.create(server, split_request[1], usr.clearance_level_id)

            elif action == "ACCESS": # usr wants to access a file
                client.access(server, console, split_request[1], split_request[2])

            elif action == "LOGOUT":
                print("Logging out...")
                server.close()
                break

            elif action in ["CLEAR", "CLS"]:
                clear()

            elif action == "HELP":
                print("Valid commands:")
                print("CREATE {filetype} - Creates a deepwell entry of the specified filetype")
                print("ACCESS {filetype} {file_id} - Accesses the specified deepwell entry")
                print("LOGOUT - Terminates the session")
                print("CLEAR (CLS) - Clears the terminal screen")

            else:
                print("INVALID COMMAND")
