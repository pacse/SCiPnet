"""
Functions to render tables from pydantic models

Contains
--------
- print_table_audit_logs: Prints a table of audit logs
- print_table_mtfs: Prints a table of mtfs
- print_table_scps: Prints a table of scps
- print_table_users: Prints a table of users
"""

from ...sql import models as Models

from tabulate import tabulate
from typing import Callable, Type, TypeVar

T = TypeVar('T')

# === Helpers ===

TABLE_CHAR_REPLACEMENTS = {
    '│': '║', '╡': '╣', '╞': '╠',
    '├': '╠', '┤': '╣', '╪': '╬',
    '┼': '╫', '╛': '╝', '╘': '╚',
    '╧': '╩', '╕': '╗', '╒': '╔',
    '╤': '╦'
}

def replace_chars(text: str) -> str:
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


def print_table(data: list[dict[str, str]]) -> None:
    """
    Prints a formatted table from a list of dicts

    Parameters
    ----------
    data : list[dict[str,str]]
        The data to be displayed in table format

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
    table_str = replace_chars(table_str).split('\n')

    # print
    for line in table_str:
        print(line)


# data formatters (not all model data is shown)
def _format_user(usr: Models.User) -> dict[str, str]:
    return {
            'ID': f'{usr.id:03d}',
            'Name': f'{usr.title.name} {usr.name}',
            'Clearance': usr.clearance_lvl.name,
            'MTF Operative': 'Yes' if usr.mtf else 'No',
            'Status': 'Active' if usr.is_active else 'Inactive'
           }


def _format_scp(scp: Models.SCP) -> dict[str, str]:
    if scp.secondary_class:
        scnd_clss = scp.secondary_class.name
    else:
        scnd_clss = 'None'

    if scp.risk_class:
        risk_clss = scp.risk_class.name
    else:
        risk_clss = '[DATA EXPUNGED]'

    if scp.disruption_class:
        disruption_clss = scp.disruption_class.name
    else:
        disruption_clss = '[DATA EXPUNGED]'

    if scp.mtf:
        mtf_name = (f'{scp.mtf.name} '
                    f'{scp.mtf.nickname!r}'
                    f'(ID: {scp.mtf.id:03d})')
    else:
        mtf_name = 'None'

    return {
            'ID': f'SCP-{scp.id:03d}',
            'Classification Level': scp.clearance_lvl.name,
            'Containment Class': f'{scp.containment_class.name}',
            'Secondary Class': scnd_clss,
            'Risk Class': risk_clss,
            'Disruption Class': disruption_clss,
            'Assigned MTF': mtf_name,
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
            'User Name': f'{log.user.name}',
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
    # valdation
    if not all(isinstance(entry, data_type) for entry in data):
        raise TypeError(f'all data entries must be {data_type.__name__}s')

    dict_data = [formatter(entry) for entry in data]

    print_table(dict_data)



# === Main functions ===

def print_table_audit_logs(data: list[Models.AuditLog]) -> None:
    _print_generic_table(Models.AuditLog, data, _format_audit_log)


def print_table_mtfs(data: list[Models.MTF]) -> None:
    _print_generic_table(Models.MTF, data, _format_mtf)


def print_table_scps(data: list[Models.SCP]) -> None:
    _print_generic_table(Models.SCP, data, _format_scp)


def print_table_users(data: list[Models.User]) -> None:
    _print_generic_table(Models.User, data, _format_user)
