from urllib.parse import unquote

from rich.markdown import Markdown as Md
from rich.console import Console

from ..sql.models import Models
from .helpers import *


# To display a SCP

def display_scp(info: Models.SCP,
                desc: str, cps: str,
                addenda: dict[str, str], console: Console
               ) -> None:
    """
    Displays a scp after requested by user
    """

    # get colours for SCP
    colours = Models.SCPColours(
        class_lvl=COLOURS[info.clearance_lvl.id],
        cont_clss=COLOURS[info.containment_class.id],
        disrupt_clss=COLOURS[info.disruption_class.id] if info.disruption_class else None,
        rsk_clss=COLOURS[info.risk_class.id] if info.risk_class else None,
    )

    # print scp_info
    acs_bar(info, colours, console)

    # print Special Containment Procedures
    console.print(Md(f'## Special Containment Procedures\n\n{cps}'))

    # print description
    console.print(Md(f'## Description\n\n{desc}'))

    # allow other file showing
    if addenda:
        a_names: list[str] = [key for key in addenda.keys()]
    else:
        a_names = []

    while True: # always offer more addenda after file access

        # make type checking happy
        i = 0

        # spacing between last print
        print()

        # check for remaining addenda
        if a_names:
            print('Display additional addenda?')

            # offer more addenda
            for i, name in enumerate(a_names):
                print(f'{i}: {unquote(name)}') # name is fname, so quoted

        print('C: close file')

        inp = input('> ')

        # process decesion
        try:
            if inp.upper() == 'C':
                return
            else:
                # get file index
                idx = int(inp)

                # access file & print
                name = a_names[idx]
                console.print(Md(f'## {unquote(name)}\n\n{addenda[name]}'))

                # don't offer it again
                a_names.remove(name)
                i -= 1

        except ValueError or IndexError:
            print(f'INVALID CHOICE: {inp!r}')


# To display a site

def display_site(info: Models.Site,
                 site_loc: str, site_desc: str,
                 additional: dict[str, str], console: Console
                ) -> None:
    """
    Displays a site after requested by user
    """

    # stuff we show later
    keys = []
    for key in additional.keys():
        if key not in ['site_info','loc','desc'] and additional[key]:
            keys.append(key)


    # first display the site bar
    site_bar(info, site_loc, console)

    # now desc
    console.print(Md(f'## Description\n\n{site_desc}'))

    # now staff table
    print_table_users(info.staff)


    # offer what we can show till f-close
    while True:

        print() # spacing

        if keys:
            print('Display additional files?')

            for i, key in enumerate(keys):
                print(f'{i}: {key}')

        print('C: close file')

        # get usr chice
        choice = input('> ')

        # handle choice
        if choice.upper() == 'C':
            return

        try:
            name = keys[int(choice)]
            console.print(Md(f'## {name}\n\n{additional[name]}'))
            keys.remove(name)

        except ValueError or IndexError:
            print(f'INVALID CHOICE: {choice!r}')


# To display a MTF

def display_mtf(info: Models.MTF, mission: str, console: Console) -> None:
    """
    displays a MTF after a user
    receives MTF info from deepwell
    """

    # as always, display the bar first
    mtf_bar(info, console)

    # now print mission
    console.print(Md(f'## Mobile Task Force Mission:\n\n{mission}'))

    # and that's it!
    print()


# to display a user

def display_user(info: Models.User, console: Console) -> None:
    # just a bar for now, no other files
    user_bar(info, console)

    print()

