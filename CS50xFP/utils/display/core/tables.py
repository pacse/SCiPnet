"""
Functions to render tables from pydantic models

Contains
--------
- print_table_audit_logs
- print_table_mtfs
- print_table_scps
- print_table_users
"""

from typing import Callable, Type, TypeVar

from tabulate import tabulate

from ...sql.transformers import Models

T = TypeVar('T')



# === Helpers ===

TABLE_CHAR_REPLACEMENTS = {
    '│': '║', '╡': '╣', '╞': '╠',
    '├': '╠', '┤': '╣', '╪': '╬',
    '┼': '╫', '╛': '╝', '╘': '╚',
    '╧': '╩', '╕': '╗', '╒': '╔',
    '╤': '╦'
}

def _replace_chars(text: str) -> str:
    """
    Replaces table characters in `text` according to
    `TABLE_CHAR_REPLACEMENTS`

    Parameters
    ----------
    text : str
        The text to replace characters in

    Returns
    -------
    str
        The text with replaced characters
    """
    for old_char, new_char in TABLE_CHAR_REPLACEMENTS.items():
        text = text.replace(old_char, new_char)
    return text

def _f_user_name(usr: Models.User) -> str:
    """Returns a user's title & name as a formatted string"""
    return f'{usr.title.name} {usr.name}'


def print_table(data: list[dict[str, str]]) -> None:
    """
    Prints a formatted table from a list of dicts

    Parameters
    ----------
    data : list[dict[str,str]]
        The data to be displayed

    Raises
    ------
    ValueError
        If `data` is empty
    TypeError
        - If any element in `data` is not a dict
        - If any key or value in the dicts is not a string
    """

    # validation
    if not data:
        raise ValueError('data must contain at least one entry')

    if not all(isinstance(entry, dict) for entry in data):
        raise TypeError('all data entries must be dicts')

    for entry in data:
        if not all(isinstance(k, str) for k in entry.keys()):
            raise TypeError('all dict keys must be strings')
        if not all(isinstance(v, str) for v in entry.values()):
            raise TypeError('all dict values must be strings')

    # Generate table with tabulate
    table_str = tabulate(
                         data,
                         headers='keys',
                         tablefmt='fancy_grid',
                         stralign='center'
                        )

    # format table
    table_str = _replace_chars(table_str).split('\n')

    # print
    for line in table_str:
        print(line)



# === Data Formatters ===

def _format_user(usr: Models.User) -> dict[str, str]:
    return {
            'ID': f'{usr.id:03d}',
            'Name': _f_user_name(usr), # .display_name includes ID
            'Clearance': usr.display_clearance,
            'MTF Operative': 'Yes' if usr.mtf_id else 'No',
            'Status': usr.display_active
           }

def _format_scp(scp: Models.SCP) -> dict[str, str]:
    return {
            'ID': scp.display_id,
            'Classification Level': scp.display_clearance,
            'Containment Class': scp.display_containment,
            'Secondary Class': scp.display_secondary,
            'Risk Class': scp.display_risk,
            'Disruption Class': scp.display_disruption,
            'Assigned MTF': scp.display_mtf,
           }

def _format_mtf(mtf: Models.MTF) -> dict[str, str]:
    return {
            'ID': f'{mtf.id:03d}',
            'Name': f"{mtf.name} '{mtf.nickname}'",
            'Active': 'Yes' if mtf.active else 'No',
           }

def _format_audit_log(log: Models.AuditLog) -> dict[str, str]:
    return {
            'User ID': f'{log.user.id:03d}',
            'User Name': _f_user_name(log.user),
            'IP Address': str(log.user_ip),
            'Action': log.action,
            'Status': 'Success' if log.status else 'Failure',
           }


def _print_generic_table(
                         data_type: Type[T],
                         data: list[T],
                         formatter: Callable[[T], dict[str, str]]
                        ) -> None:
    """
    A generic table printer

    **NOT TO BE IMPORTED OR USED OUTSIDE `tables.py`**
    """
    # validation
    if not data:
        raise ValueError('data must contain at least one entry')

    if not all(isinstance(entry, data_type) for entry in data):
        raise TypeError(f'all data entries must be {data_type.__name__}s')

    dict_data = [formatter(entry) for entry in data]

    print_table(dict_data)



# === Main functions ===

def print_table_audit_logs(data: list[Models.AuditLog]) -> None:
    """
    Prints a table of audit logs

    Parameters
    ----------
    data : list[Models.AuditLog]
        The audit logs to be displayed

    Raises
    ------
    ValueError
        If `data` is empty
    TypeError
        If any element in `data` is not an AuditLog

    """
    _print_generic_table(Models.AuditLog, data, _format_audit_log)

def print_table_mtfs(data: list[Models.MTF]) -> None:
    """
    Prints a table of MTFs

    Parameters
    ----------
    data : list[Models.MTF]
        The MTFs to be displayed

    Raises
    ------
    ValueError
        If `data` is empty
    TypeError
        If any element in `data` is not a MTF

    """
    _print_generic_table(Models.MTF, data, _format_mtf)

def print_table_scps(data: list[Models.SCP]) -> None:
    """
    Prints a table of SCPs

    Parameters
    ----------
    data : list[Models.SCP]
        The SCPs to be displayed

    Raises
    ------
    ValueError
        If `data` is empty
    TypeError
        If any element in `data` is not a SCP

    """
    _print_generic_table(Models.SCP, data, _format_scp)

def print_table_users(data: list[Models.User]) -> None:
    """
    Prints a table of users

    Parameters
    ----------
    data : list[Models.User]
        The users to be displayed

    Raises
    ------
    ValueError
        If `data` is empty
    TypeError
        If any element in `data` is not a User

    """

    _print_generic_table(Models.User, data, _format_user)



# === Exports ===

__all__ = [
           'print_table_audit_logs',
           'print_table_mtfs',
           'print_table_scps',
           'print_table_users'
          ]
