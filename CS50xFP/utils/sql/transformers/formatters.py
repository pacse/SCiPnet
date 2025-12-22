"""
Formatting utils for data display

Contains
--------
- ID formatters (FormatIDs)
    - format_scp_id()
    - format_mtf_id()
    - format_site_id()

- Name formatters (FormatNames)
    - format_mtf_name()
    - format_site_name()
    - format_user_name()
"""

# === ID formatters ===

def _format_id(
               prefix: str,
               id: int,
               length: int = 3
              ) -> str:
    """
    Formats an ID for display

    Parameters
    ----------
    prefix : str
        The type of ID (e.g., 'SCP', 'MTF', 'Site')
    id : int
        The ID number
    length : int = 3
        The length of the numeric part

    Returns
    -------
    str
        The formatted ID: f'{prefix}-{id:0{length}d}'
    """
    # validation handled by pydantic

    return f'{prefix}-{id:0{length}d}'

def format_scp_id(id: int) -> str:
    """
    Formats an SCP ID for display

    Parameters
    ----------
    id : int
        The SCP ID number

    Returns
    -------
    str
        The formatted SCP ID: f'SCP-{id:03d}'
    """
    return _format_id('SCP', id)

def format_mtf_id(id: int) -> str:
    """
    Formats an MTF ID for display

    Parameters
    ----------
    id : int
        The MTF ID number

    Returns
    -------
    str
        The formatted MTF ID: f'MTF-{id:03d}'
    """
    return _format_id('MTF', id)

def format_site_id(id: int) -> str:
    """
    Formats a Site ID for display

    Parameters
    ----------
    id : int
        The Site ID number

    Returns
    -------
    str
        The formatted Site ID: f'Site-{id:03d}'
    """
    return _format_id('Site', id)



# === Name formatters ===

def _format_name(
                 name: str,
                 id: int,
                 prefix: str = '',
                 id_length: int = 3
                ) -> str:
    """
    Formats a name with ID for display

    Parameters
    ----------
    name : str
        The name
    id : int
        The ID number
    prefix : str = ''
        The prefix for the ID (e.g. 'MTF')
    id_length : int = 3
        The length of the numeric part of the ID

    Returns
    -------
    str
        The formatted name with ID:
        `f'{name} (ID\\: {id:0{id_length}d})' if prefix == ''`

        or `f'{prefix} {name} (ID\\: {id:0{id_length}d})' if prefix != ''`

        (Colons are escaped for Rich md rendering)
    """
    # validation handled by pydantic

    if prefix == '':
        return f'{name} (ID\\: {id:0{id_length}d})'
    return f'{prefix} {name} (ID\\: {id:0{id_length}d})'

def format_mtf_name(name: str, id: int, nickname: str | None = None) -> str:
    """
    Formats an MTF name with ID for display

    Parameters
    ----------
    name : str
        The MTF name
    id : int
        The MTF ID number
    nickname : str | None = None
        The MTF nickname

    Returns
    -------
    str
        The formatted MTF name with ID:
        f'MTF {name} (ID\\: {id})' if no nickname
        f'MTF {name} "{nickname}" (ID\\: {id})' if nickname present
        (Colons are escaped for Rich md rendering)
    """
    if nickname:
        return _format_name(f'{name} "{nickname}"', id)
    return _format_name(name, id, 'MTF')

def format_site_name(name: str, id: int) -> str:
    """
    Formats a Site name with ID for display

    Parameters
    ----------
    name : str
        The Site name
    id : int
        The Site ID number

    Returns
    -------
    str
        The formatted Site name with ID:
        f'{name} (ID\\: {id:03d})'
        (Colons are escaped for Rich md rendering)
    """
    return _format_name(name, id)

def format_user_name(title: str, name: str, id: int) -> str:
    """
    Formats a User name with ID for display

    Parameters
    ----------
    title : str
        The User's title
    name : str
        The User's name
    id : int
        The User ID number

    Returns
    -------
    str
        The formatted User name with ID:
        f'{title} {name} (ID\\: {id})'
        (Colons are escaped for Rich md rendering)
    """
    return _format_name(name, id, title)



# === Exports ===

class FormatIDs:
    scp = staticmethod(format_scp_id)
    mtf = staticmethod(format_mtf_id)
    site = staticmethod(format_site_id)

class FormatNames:
    mtf = staticmethod(format_mtf_name)
    site = staticmethod(format_site_name)
    user = staticmethod(format_user_name)

__all__ = [
           'FormatIDs',
           'FormatNames',

           'format_scp_id',
           'format_mtf_id',
           'format_site_id',

           'format_mtf_name',
           'format_site_name',
           'format_user_name',
          ]
