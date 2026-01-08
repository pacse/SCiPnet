"""
Helper funcs

Contains
--------
- read_file(path: Path | str, encoding: str = 'utf-8') -> str
- read_files(parent_dir: Path, files: list[str] | None = None, encoding: str = 'utf-8') -> dict[str, str]
"""

import os
from pathlib import Path
from ..general.sql_config import EXPUNGED
from ..sql.queries import log_event



def read_file(
              path: Path,
              encoding: str = 'utf-8'
             ) -> str:
    """
    Reads a text file

    Parameters
    ----------
    path : Path | str
        The full file path
    encoding : str = 'utf-8'
        The encoding to pass to `open()`

    Returns
    -------
    str
        The result of `f.read()` or `EXPUNGED` if `path` not found
    """
    if not path.exists():
        return EXPUNGED
    return path.read_text(encoding=encoding)


def read_files(
               parent_dir: Path,
               files: list[str] | None = None,
               encoding: str = 'utf-8'
              ) -> dict[str, str]:
    """
    Reads text files from `parent_dir`

    Parameters
    ----------
    parent_dir: Path | str
        The directory that contains `paths`
    files : list[str] | None = None
        The local file names. If ommited, reads all files in `parent_dir`
    encoding : str = 'utf-8'
        The encoding to pass to `open()`

    Returns
    -------
    dict[str, str]
        a dict with keys as `paths` and items as file data

    Notes
    -----
    - Reads files as so: `parent_dir / file`
    - If file not found, file data is `EXPUNGED`
    - If `parent_dir` does not exist, all file datas are `EXPUNGED`
    """
    result = {}

    if not parent_dir.exists():
        return {f: EXPUNGED for f in files or []}

    if not files:
        files = [f.name for f in parent_dir.iterdir()]


    return {f: read_file(parent_dir / f, encoding) for f in files}


def log_access(
               user_id: int,
               user_ip: str,
               status: bool,
               details: str,
              ) -> None:
    """
    Helper to log access attempts

    Parameters
    ----------
    user_id : int
        The user's ID
    user_ip : str
        The user's IP address
    status : bool
        The access status
    details : str
        The access details

    Notes
    -----
    - Does not validate parameters
    - A wrapper for `sql.queries.log_event()`
    """
    log_event(
            user_id=user_id,
            user_ip=user_ip,
            action='File Access',
            details=details,
            status=status
        )


__all__ = ['read_file', 'read_files', 'log_access']