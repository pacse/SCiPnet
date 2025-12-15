"""
Display functions for files

Contains
--------
- display_scp()
- display_site()
- display_mtf()
- display_user()
"""

from urllib.parse import unquote

from rich.console import Console

from .core.bars import acs_bar, site_bar, mtf_bar, user_bar
from .core.tables import print_table_users, print_table_mtfs, \
                         print_table_scps
from ..sql.models import Models
from .helpers import print_md, print_md_title, check_type_and_empty_str
from ..sql.null_processors import ProcessedData as PD


def _display_additional_files(
                              additional: dict[str, str],
                              console: Console
                             ) -> None:
    """
    Handles logic for displaying additional files for SCPs and Sites

    Parameters
    ----------
    additional : dict[str, str]
        Additional files to display: key is file name, value is file content
    console : Console
        Rich console to print to

    Raises
    ------
    TypeError
        - If `additional` is not a dict[str, str]
        - If `console` is not a rich Console instance
    ValueError
        - If any file name or content in `additional` is an empty string
    """

    # validation
    if not isinstance(additional, dict):
        raise TypeError('`additional` must be a dict[str, str]')
    elif not all(isinstance(k, str) and isinstance(v, str)
                 for k, v in additional.items()):
        raise TypeError('All keys and values in `additional` must be strings')

    if not isinstance(console, Console):
        raise TypeError('`console` must be a rich Console instance')


    # logic
    if additional:
        names = [key for key in additional.keys()]
    else:
        names = []


    while True: # keep offering files till user closes

        if names:
            print('\nDisplay additional files?')

        for i, name in enumerate(names):
            print(f'{i}: {unquote(name)}') # name is fname, so quoted

        print('C: close file')

        inp = input('> ')

        # process decesion
        try:
            if inp.upper() == 'C':
                print() # end with a newline
                return
            else:
                # get file index
                idx = int(inp)

                # access file & print
                name = names[idx]
                print_md_title(unquote(name), additional[name], console)

                # don't offer it again
                names.remove(name)

        except (ValueError, IndexError):
            print(f'INVALID CHOICE: {inp!r}')



def display_scp(
                info: PD.SCP,
                desc: str,
                cps: str,
                addenda: dict[str, str],
                console: Console
               ) -> None:
    """
    Displays a SCP

    Parameters
    ----------
    info : ProcessedData.SCP
        SCP info to display
    desc : str
        SCP description to display
    cps : str
        SCP special containment procedures to display
    addenda : dict[str, str]
        Additional files to display
    console : Console
        Rich console to print to

    Raises
    ------
    TypeError
        - If `info` is not a ProcessedData.SCP instance
        - If `desc` is not a string
        - If `cps` is not a string
        - If `addenda` is not a dict[str, str]
        - If `console` is not a rich Console instance
    ValueError
        - If `desc` is an empty string
        - If `cps` is an empty string
    """

    # validation
    if not isinstance(info, PD.SCP):
        raise TypeError('`info` must be a ProcessedData.SCP instance')

    check_type_and_empty_str(desc, 'desc')
    check_type_and_empty_str(cps, 'cps')

    if not isinstance(addenda, dict):
        raise TypeError('`addenda` must be a dict[str, str]')
    elif not all(isinstance(k, str) and isinstance(v, str)
                 for k, v in addenda.items()):
        raise TypeError('All keys and values in `addenda` must be strings')

    if not isinstance(console, Console):
        raise TypeError('`console` must be a rich Console instance')


    # print scp_info
    acs_bar(info, console)

    # print Special Containment Procedures
    print_md_title('Special Containment Procedures', cps, console)

    # print description
    print_md_title('Description', desc, console)

    # print additional files
    _display_additional_files(addenda, console)


def display_site(
                 info: PD.Site,
                 site_loc: str,
                 site_desc: str,
                 staff: list[Models.User],
                 mtfs: list[Models.MTF],
                 scps: list[Models.SCP],
                 additional: dict[str, str],
                 console: Console,
                ) -> None:
    """
    Displays a Site

    Parameters
    ----------
    info : ProcessedData.Site
        Site info to display
    site_loc : str
        Site location to display
    site_desc : str
        Site description to display

    staff : list[Models.User]
        Site staff to display
    mtfs : list[Models.MTF]
        Site MTFs to display
    scps : list[Models.SCP]
        Site SCPs to display

    additional : dict[str, str]
        Additional files to display
    console : Console
        Rich console to print to

    Raises
    ------
    TypeError
        - If `info` is not a ProcessedData.Site instance
        - If `site_loc` is not a string
        - If `site_desc` is not a string
        - If `additional` is not a dict[str, str]
        - If `console` is not a rich Console instance
    ValueError
        - If `site_loc` is an empty string
        - If `site_desc` is an empty string
    """

    # validation
    if not isinstance(info, PD.Site):
        raise TypeError('`info` must be a ProcessedData.Site instance')

    check_type_and_empty_str(site_loc, 'site_loc')
    check_type_and_empty_str(site_desc, 'site_desc')

    if not isinstance(additional, dict):
        raise TypeError('`additional` must be a dict[str, str]')
    elif not all(isinstance(k, str) and isinstance(v, str)
                 for k, v in additional.items()):
        raise TypeError('All keys and values in `additional` must be strings')

    if not isinstance(console, Console):
        raise TypeError('`console` must be a rich Console instance')


    # first display the site bar
    site_bar(info, site_loc, console)

    # now desc
    print_md_title('Site Description', site_desc, console)

    # now tables
    print_md('## Site Staff', console)
    print_table_users(staff)

    print_md('## Site MTFs', console)
    print_table_mtfs(mtfs)

    print_md('## Site SCPs', console)
    print_table_scps(scps)

    # now additional files
    _display_additional_files(additional, console)


def display_mtf(
                info: PD.MTF,
                mission: str,
                console: Console
               ) -> None:
    """
    displays a MTF

    Parameters
    ----------
    info : ProcessedData.MTF
        MTF info to display
    mission : str
        MTF mission to display
    console : Console
        Rich console to print to

    Raises
    ------
    TypeError
        - If `info` is not a ProcessedData.MTF instance
        - If `mission` is not a string
        - If `console` is not a rich Console instance
    ValueError
        - If `mission` is an empty string
    """

    # validation
    if not isinstance(info, PD.MTF):
        raise TypeError('`info` must be a ProcessedData.MTF instance')

    check_type_and_empty_str(mission, 'mission')

    if not isinstance(console, Console):
        raise TypeError('`console` must be a rich Console instance')


    # as always, display the bar first
    mtf_bar(info, console)

    # now print mission
    print_md_title('Mobile Task Force Mission', mission, console)

    # and that's it!
    print()


def display_user(info: PD.User, console: Console) -> None:
    """
    Displays a User

    Parameters
    ----------
    info : ProcessedData.User
        User info to display
    console : Console
        Rich console to print to

    Raises
    ------
    TypeError
        - If `info` is not a ProcessedData.User instance
        - If `console` is not a rich Console instance
    """

    # validation
    if not isinstance(info, PD.User):
        raise TypeError('`info` must be a ProcessedData.User instance')
    if not isinstance(console, Console):
        raise TypeError('`console` must be a rich Console instance')


    # just a bar for now, no other files
    user_bar(info, console)

    print()

