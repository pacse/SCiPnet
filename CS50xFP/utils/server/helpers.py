"""
Helpers for server operations

Contains
--------
- auth_usr(id: int, password: str) -> tuple[bool, PydanticModels.User | None]
- access(f_type: str, f_id: int, user: PydanticModels.User, user_ip: str) -> Message
"""

import os
from werkzeug.security import check_password_hash
from pathlib import Path
from typing import Any, Literal

from ..general.server_config import Server
from ..general.display_config import Styles
from ..general.sql_config import DEEPWELL_DIR
from ..general.validation import validate_int, validate_ip, validate_str, \
                                 validate_field

from ..sql.queries import get_model, get_field, log_event
from ..sql.transformers import Models as PydanticModels, orm_to_pydantic
from ..sql.schema import MainModels as ORMModels, \
                         HelperModels as ORMHelperModels
from ..socket.protocol import Message
from ..socket import Msg
from ..general.exceptions import RecordNotFoundError
from ..general.sql_config import EXPUNGED



def _read_file(
        path: Path | str,
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
    if not os.path.exists(path):
        return EXPUNGED

    with open(path, encoding=encoding) as f:
        return f.read()


def _read_files(
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

    if not files:
        files = os.listdir(parent_dir)

    if not os.path.exists(parent_dir):
        for f in files:
            result[f] = EXPUNGED

    else:
        for path in files:
            result[path] = _read_file(
                parent_dir / path, encoding=encoding
            )

    return result



# === Main Funcs ===

def auth_usr(
             user_id: int,
             password: str
            ) -> tuple[bool, PydanticModels.User | None]:
    """
    Authenticates a user

    Parameters
    ----------
    user_id : int
        The user's ID
    password : str
        The password to authenticate (TODO: Expect hashed password)

    Returns
    -------
    tuple[bool, PydanticModels.User | None]
        - Whether authentication was successful
        - The user data if successful, else None

    Raises
    ------
    TypeError
        - If `user_id` is not an int
        - If `password` is not a str
    ValueError
        - If `user_id` is not positive
        - If `password` is empty or whitespace-only
    """

    if Server.DEBUG:
        print(
            f'Authenticating user {user_id!r} with password: {password!r}'
        )

    validate_int('user_id', user_id)
    validate_str('password', password)

    user = get_model(ORMModels.User, user_id)

    if user and check_password_hash(str(user.password), password):
        if Server.DEBUG:
            print(f'Sucess, returning: True, {user}')
        return True, orm_to_pydantic(user)
    else:
        if Server.DEBUG:
            print('Falure, returning: False, None')
        return False, None # return False and None



def access(
           f_type: str,
           f_id: int,
           user: PydanticModels.User,
           user_ip: str
          ) -> Message:

    # === validation ===

    validate_str('f_type', f_type)
    validate_int('f_id', f_id)
    validate_field('user', user, PydanticModels.User)
    validate_ip('user_ip', user_ip)



    # === get file data ===

    f_model_class = Server.VALID_F_TYPES.get(f_type.upper())

    if not f_model_class:
        log_event(
            user_id=user.id,
            user_ip=user_ip,
            action='File Access Attempt',
            details=f'Attempted access to invalid file type: {f_type}',
            status=False
        )
        return Msg.access_type_fail(f_type)

    try:
        f_data = get_model(f_model_class, f_id)
        f_model = orm_to_pydantic(f_data)
    except RecordNotFoundError:
        log_event(
            user_id=user.id,
            user_ip=user_ip,
            action='File Access Attempt',
            details=f'Attempted access to non-existent {f_type} ID {f_id}',
            status=False
        )
        return Msg.access_expunged(f_type, f_id)



    # === Check clearance ===

    if isinstance(
        f_model,
        (PydanticModels.SCP, PydanticModels.User)
    ) and user.clearance_lvl.id < f_model.clearance_lvl.id:
        log_event(
            user_id=user.id,
            user_ip=user_ip,
            action='File Access Attempt',
            details=(
                f'Attempted access to {f_type} ID {f_id} with'
                ' insufficient clearance'
            ),
            status=False
        )
        return Msg.access_redacted(
            user.display_clearance,
            Styles.CLEAR_LVL[user.clearance_lvl.id],
            f_model.display_clearance,
            Styles.CLEAR_LVL[f_model.clearance_lvl.id],
        )

    elif isinstance(
        f_model, PydanticModels.Site
    ) and (user.clearance_lvl.id < 3 and user.site_id != f_model.id):
        log_event(
            user_id=user.id,
            user_ip=user_ip,
            action='File Access Attempt',
            details=(
                f'Attempted access to Site {f_model.id} with'
                ' insufficient clearance'
            ),
            status=False
        )
        return Msg.access_redacted(
            user.display_clearance,
            Styles.CLEAR_LVL[user.clearance_lvl.id],
            get_field(ORMHelperModels.ClearanceLvl, 'name', 'id', 3),
            Styles.CLEAR_LVL[3],
        )



    # === Gather file data ===

    data: dict[str, Any] = {'f_model': f_model.model_dump_json()}

    f_path = (DEEPWELL_DIR / f'{f_type.lower()}s' / f'{f_id}').resolve()

    if isinstance(f_model, PydanticModels.SCP):

        # get desc & special containment procedures
        files = _read_files(f_path, ['desc.md', 'cps.md'])

        # get addenda
        addenda = _read_files(f_path / 'addenda')

        # add to data
        data['addenda'] = addenda
        data.update(files)


    elif isinstance(f_model, PydanticModels.MTF):

        # get mission
        path = f_path / 'mission.md'
        mission = _read_file(path)

        # add to data
        data['mission.md'] = mission

    elif isinstance(f_model, PydanticModels.Site):

        # get location, desc & dossier
        files = _read_files(
            f_path,
            ['loc.md', 'desc.md', 'dossier.md']
        )

        # add to data
        data.update(files)



    # === Return ===

    log_event(
        user_id=user.id,
        user_ip=user_ip,
        action='File Access Attempt',
        details=(
            f'Accessed {f_type} {f_model.id}'
        ),
        status=True
    )

    return Msg.access_granted(data)

