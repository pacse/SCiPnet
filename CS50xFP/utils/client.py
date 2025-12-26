'''
Client side utility functions
'''
import socket
from werkzeug.security import generate_password_hash

from .art import *
from .socket.transport import ADDR, send, recv

# for typedefing
from rich.console import Console
from typing import Any

def conn_to_server() -> socket.socket:
    '''
    Establishes connection to server
    '''
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(ADDR) # connect to server
    return s


def create(server: socket.socket, f_type: str, c_lvl: int) -> None:
    '''
    Adds a {type} entry to the deepewell
    '''

    # warn usr actions are logged
    printc("WARNING: ACTIONS ARE LOGGED")

    if input("Continue? (y/n)\n>>> ").lower() != "y":
        return

    # Send server create request
    send(server, f"CREATE {f_type}")

    # get response
    response = recv(server)

    # check for errors
    if not response: # ensure we have data
        no_response()
        return

    if len(response) == 3: # clearance error
        clearance_denied(response[1], response[2])
        return

    elif len(response) == 2: # invalid f-type
        invalid_f_type(response[1])

    elif response == "RENDER": # all clear
        create_f(f_type)

    # get necessary info for creation
    create_info = recv(server)

    if not create_info:
        no_response()
        return

    # get file data from usr
    file = {}

    if f_type == "SCP":
        # scp_id
        file["id"] = 3 #int(input(f"ID (next id: {create_info['id']}) >>> "))

        # show available classification lvls
        printc("Classification Levels:")
        for c_level in create_info["clearance_levels"]:
            print(f"{c_level['id']} - {c_level['name']}")
        print()

        # get file classification lvl
        file["classification_level_id"] = 1 #int(input("Classification Level (id)\n>>> "))

        # show available containment classes
        printc("Containment Classes:")
        for c_class in create_info["containment_classes"]:
            print(f"{c_class['id']} - {c_class['name']}")
        print()

        # get file containment class
        file["containment_class_id"] = 1 #int(input("Containment Class (id)\n>>> "))

        # show available secondary classes
        printc("Secondary Classes:")
        for s_class in create_info["secondary_classes"]:
            print(f"{s_class['id']} - {s_class['name']}")
        print()

        # get file secondary class
        file["secondary_class_id"] = 0 #int(input("Secondary Class (id)\n>>> "))

        # show available disruption classes
        printc("Disruption Classes:")
        for d_class in create_info["disruption_classes"]:
            print(f"{d_class['id']} - {d_class['name']}")
        print()

        # get file disruption class
        file["disruption_class_id"] = 1 #int(input("Disruption Class (id)\n>>> "))


        # show available risk classes
        printc("Risk Classes:")
        for r_class in create_info["risk_classes"]:
            print(f"{r_class['id']} - {r_class['name']}")
        print()

        # get file risk class
        file["risk_class_id"] = 1 #int(input("Risk Class (id)\n>>> "))

        print()
        # get site responsible
        file["site_responsible_id"] = 1123 #int(input("Site Responsible (id)\n>>> "))
        print()
        # get assigned task force
        file["atf_id"] = 1 #input("Assigned Task Force (id)\n>>> ")
        if not file["atf_id"]: # if no atf, set to None
            file["atf_id"] = "None"
        else:
            file["atf_id"] = int(file["atf_id"])
        print()
        # get special containment procedures
        file["SCPs"] = "1" #input("Special Containment Procedures\n>>> ")
        print()
        # get description
        file["desc"] = "1" #input("Description\n>>> ")
        print()
        # TODO: Handle addenda and multi descs/SCPs

    elif f_type == "MTF":
        file["name"] = input("MTF Name (eg. Epsilon-6)\n>>> ")
        print()
        file["nickname"] = input("MTF Nickname (eg. Village Idiots)\n>>> ")
        print()
        file["leader"] = int(input("MTF Leader (user id)\n>>> "))
        print()
        file["desc"] = input("MTF Description\n>>> ")
        # TODO: Handle ect files

    elif f_type == "SITE":
        file["name"] = input("Site Name (eg. Humanoid Containment Site-06-3)\n>>> ")
        print()
        file["director"] = int(input("Site Director (id)\n>>> "))
        print()
        file["loc"] = input("Location (eg. Lorraine, Grand Est, France | 48.723° N, 6.264° E)\n>>> ")
        print()
        file["desc"] = input("Site Description\n>>> ")
        print()
        file["dossier"] = input("Site Dossier (Enter 'None' if not applicable)\n>>> ")

    elif f_type == "USER":
        file["name"] = input("Name\n>>> ")
        print()
        file["password"] = generate_password_hash(input("Password\n>>> "))
        print()

        # show available clearance lvls
        printc("Clearance Levels:")
        for c_level in create_info["clearance_levels"]:
            print(f"{c_level['id']} - {c_level['name']}")

        # get clearance level
        file["clearance_level_id"] = int(input(f"Clearance Level (max: {c_lvl-1 if c_lvl < 6 else 6})\n>>> "))

        print()

        # show available titles
        printc("Titles:")
        for title in create_info["titles"]:
            print(f"{title['id']} - {title['name']}")

        # get title
        file["title_id"] = int(input("Title (id)\n>>> "))
        print()
        file["site_id"] = int(input("Assigned Site (id)\n>>> "))
        print()
        # only clearance 3+ users get a phrase
        if file["clearance_level_id"] >= 3:
            file["override_phrase"] = generate_password_hash(input("Override Phrase\n>>> "))
        else:
            file["override_phrase"] = None
        print()

    # send to server
    send(server, file)

    # check for all clear
    all_clear = recv(server)

    if not all_clear:
        no_response()
        return


    if all_clear == "INVALID FILE DATA":
        invalid_f_data()

    elif all_clear == "NO DATA RECEIVED":
        no_data_recvd()

    elif all_clear == "CREATED":
        created_f(f_type)


def access(server: socket.socket, console: Console, type: str, file: str) -> None:

    # send server access request
    send(server, f"ACCESS {type} {file}")

    # get response
    response = recv(server)
    if not response: # ensure we have data
        no_response()
        server.close()
        return

    # check for errors
    if response == "INVALID FILETYPE":
        invalid_f_type(type)
        return

    elif response == "EXPUNGED":
        expunged(f"{type} {file}")
        return

    elif response[0] == "REDACTED":
        redacted(f"{type} {file}", response[1], response[2])
        return

    elif response[0] != "GRANTED":
        printc(f"INVALID RESPONSE: {response!r}")
        server.close()
        return

    f_data: dict[str, Any] = response[1]

    if type == "SCP":
        display_scp(f_data, console)

    elif type == "MTF":
        display_mtf(f_data, console)
    elif type == "SITE":
        display_site(f_data, console)

    elif type == "USER":
        display_user(f_data, console)
    else:
        # TODO: Better message
        printc(f"INVALID F_TYPE: {type!r}")
