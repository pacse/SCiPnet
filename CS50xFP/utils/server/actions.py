"""
Handlers for server response to actions

Contains
--------
- access(f_type: str, f_id: int, user: PydanticModels.User, user_ip: str) -> Message
"""

from typing import Literal

from .helpers import read_file, read_files, log_access
from ..general.server_config import Server
from ..general.display_config import Styles
from ..general.sql_config import DEEPWELL_DIR
from ..general.validation import validate_int, validate_ip, validate_field, \
                                 validate_f_type

from ..sql.queries import get_model, get_field, db_session
from ..sql.transformers import Models as PydanticModels, orm_to_pydantic
from ..sql.schema import HelperModels as ORMHelperModels
from ..socket.protocol import Message, AccessGrantedSCPData, \
                              AccessGrantedMTFData, AccessGrantedSiteData, \
                              AccessGrantedUserData
from ..socket import Msg
from ..general.exceptions import RecordNotFoundError




# === Main Funcs ===


def access(
           f_type: Literal['SCP', 'MTF', 'SITE', 'USER'],
           f_id: int,
           user: PydanticModels.User,
           user_ip: str
          ) -> Message:
    """
    Accesses a file for a user if they have sufficient clearance

    Parameters
    ----------
    f_type : Literal['SCP', 'MTF', 'SITE', 'USER']
        The file type
    f_id : int
        The file ID
    user : PydanticModels.User
        The user requesting access
    user_ip : str
        The user's IP address

    Returns
    -------
    Message
        The appropriate access message
    """
    validate_f_type(f_type)
    validate_int('f_id', f_id, False, False)
    validate_field('user', user, PydanticModels.User)
    validate_ip('user_ip', user_ip)


    # === get file data ===

    f_model_class = Server.VALID_F_TYPES.get(f_type)

    if not f_model_class:
        log_access(
            user.id, user_ip, False,
            f'Attempted access to invalid file type: {f_type}'
        )
        return Msg.access_type_fail(f_type)

    with db_session() as session:
        f_data = session.get(f_model_class, f_id)
        if not f_data:
            log_access(
                user.id, user_ip, False,
                f'Attempted access to non-existent {f_type} ID {f_id}'
            )
            return Msg.access_expunged(f_type, f_id)

        f_model = orm_to_pydantic(f_data)


    # === Check clearance ===

    if isinstance(
        f_model,
        (PydanticModels.SCP, PydanticModels.User)
    ) and user.clearance_lvl.id < f_model.clearance_lvl.id:
        log_access(
            user.id, user_ip, False,
            f'Attempted access to {f_type} ID {f_id}'
             ' with insufficient clearance'
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
        log_access(
            user.id, user_ip, False,
            f'Attempted access to Site {f_model.id} with'
                ' insufficient clearance'
        )
        return Msg.access_redacted(
            user.display_clearance,
            Styles.CLEAR_LVL[user.clearance_lvl.id],
            get_field(ORMHelperModels.ClearanceLvl, 'name', 'id', 3),
            Styles.CLEAR_LVL[3],
        )

    # MTF's are accessible to all authenticated users for now


    # === Gather file data ===

    f_path = (DEEPWELL_DIR / f'{f_type.lower()}s' / f'{f_id}').resolve()


    if isinstance(f_model, PydanticModels.SCP):
        scp_data: AccessGrantedSCPData = {
            'f_type': 'SCP',
            'f_model': f_model.model_dump_json(),
            'files': {
                'desc': read_file(f_path / 'desc.md'),
                'cps': read_file(f_path / 'cps.md'),
                'addenda': read_files(f_path / 'addenda'),
            },
        }
        result = Msg.access_granted(scp_data)

    elif isinstance(f_model, PydanticModels.MTF):
        mtf_data: AccessGrantedMTFData = {
            'f_type': 'MTF',
            'f_model': f_model.model_dump_json(),
            'files': {
                'mission': read_file(f_path / 'mission.md'),
            },
        }
        result = Msg.access_granted(mtf_data)

    elif isinstance(f_model, PydanticModels.Site):
        site_data: AccessGrantedSiteData = {
            'f_type': 'SITE',
            'f_model': f_model.model_dump_json(),
            'files': {
                'loc': read_file(f_path / 'loc.md'),
                'desc': read_file(f_path / 'desc.md'),
                'dossier': read_file(f_path / 'dossier.md'),
            },
        }
        result = Msg.access_granted(site_data)

    else:
        user_data: AccessGrantedUserData = {
            'f_type': 'USER',
            'f_model': f_model.model_dump_json(),
            'files': {
                # Users have no associated files
            },
        }
        result = Msg.access_granted(user_data)


    # === Log & Return ===

    log_access(
        user.id, user_ip, True,
        f'Accessed {f_type} {f_model.id}'
    )
    return result



# === Exports ===

__all__ = [
    'access',
]
