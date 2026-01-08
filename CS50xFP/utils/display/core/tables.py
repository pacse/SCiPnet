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

from ...sql.transformers.formatters import FormatIDs
from ...sql.transformers import Models, RefModels
from ...general.sql_config import NONE_STR, EXPUNGED

T = TypeVar('T')



# === Helpers ===

TABLE_CHAR_REPLACEMENTS = {
    '│': '║', '╡': '╣', '╞': '╠',
    '├': '╠', '┤': '╣', '╪': '╬',
    '┼': '╫', '╛': '╝', '╘': '╚',
    '╧': '╩', '╕': '╗', '╒': '╔',
    '╤': '╦', '─': '═', '╫': '╬'
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

def _format_user(usr: Models.User | RefModels.User) -> dict[str, str]:
    """Formats a User for table display"""
    has_mtf = getattr(usr, 'mtf_id', None) is not None

    return {
            'ID': f'{usr.id:03d}',
            'Name': f'{usr.title.name} {usr.name}',
            'Clearance': usr.clearance_lvl.name,
            'MTF Operative': 'Yes' if has_mtf else 'No',
            'Status': 'Active' if usr.is_active else 'Inactive'
           }

def _format_scp(scp: Models.SCP | RefModels.SCP) -> dict[str, str]:
    """Formats a SCP for table display"""
    secondary = getattr(scp, 'secondary_class', None)
    disruption = getattr(scp, 'disruption_class', None)
    risk = getattr(scp, 'risk_class', None)

    return {
            'ID': FormatIDs.scp(scp.id),
            'Classification Level': scp.clearance_lvl.name,
            'Containment Class': scp.containment_class.name,
            'Secondary Class': secondary.name if secondary else NONE_STR,
            'Risk Class': risk.name if risk else EXPUNGED,
            'Disruption Class': disruption.name if disruption else EXPUNGED,
            'Assigned MTF': scp.mtf.name if scp.mtf else NONE_STR,
           }

def _format_mtf(mtf: Models.MTF | RefModels.MTF) -> dict[str, str]:
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
    _print_generic_table(data, _format_audit_log)

def print_table_mtfs(data: list[Models.MTF | RefModels.MTF]) -> None:
    """
    Prints a table of MTFs

    Parameters
    ----------
    data : list[Models.MTF | RefModels.MTF]
        The MTFs to be displayed

    Raises
    ------
    ValueError
        If `data` is empty
    TypeError
        If any element in `data` is not a MTF

    """
    _print_generic_table(data, _format_mtf)

def print_table_scps(data: list[Models.SCP | RefModels.SCP]) -> None:
    """
    Prints a table of SCPs

    Parameters
    ----------
    data : list[Models.SCP | RefModels.SCP]
        The SCPs to be displayed

    Raises
    ------
    ValueError
        If `data` is empty
    TypeError
        If any element in `data` is not a SCP

    """
    _print_generic_table(data, _format_scp)

def print_table_users(data: list[Models.User | RefModels.User]) -> None:
    """
    Prints a table of users

    Parameters
    ----------
    data : list[Models.User | RefModels.User]
        The users to be displayed

    Raises
    ------
    ValueError
        If `data` is empty
    TypeError
        If any element in `data` is not a User

    """
    _print_generic_table(data, _format_user)



# === Exports ===

__all__ = [
           'print_table_audit_logs',
           'print_table_mtfs',
           'print_table_scps',
           'print_table_users'
          ]
