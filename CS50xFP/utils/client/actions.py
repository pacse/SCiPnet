import socket

from rich.console import Console

from ..general.validation import validate_f_type, validate_int, \
                                 validate_field, validate_msg

from ..socket import send, recv, MessageTypes
from ..socket.protocol import AccessMessages

from ..display.create import no_response
from ..display.access import expunged, redacted, granted, invalid_response
from ..display.displays import display_scp, display_mtf, display_site, \
                               display_user

from ..sql.transformers.models import SCP, MTF, Site, User


def access(
           server: socket.socket,
           console: Console,
           f_type: str,
           f_id: int
          ) -> None:
    """
    Handles file access requests to the server

    Parameters
    ----------
    server : socket.socket
        the connected server socket
    console : Console
        the rich console to display to
    f_type :
        the type of file being accessed ('SCP', 'MTF', 'SITE', or 'USER')
    f_id : int
        the ID of the file being accessed

    Raises
    ------
    TypeError
        - If `server` is not a `socket.socket`
        - If `console` is not a `Console`
        - If `f_id` is not an integer
    ValueError
        - If `f_type` is not in `['SCP', 'MTF', 'SITE', 'USER']`
        - If `f_id` is negative
    """
    validate_field('server', server, socket.socket)
    validate_field('console', console, Console)
    validate_f_type(f_type)
    validate_int('f_id', f_id, False, False)


    # send access request
    send(
        server, MessageTypes.ACCESS_REQUEST,
        {'f_type': f_type, 'f_id': f_id}
    )

    response = validate_msg(recv(server), AccessMessages) # type: ignore[arg-type]

    # handle response
    if not response:
        no_response()
        return

    msg_data = response['data']

    match response['type']:
        case MessageTypes.ACCESS_EXPUNGED:
            expunged(f_type, f_id)

        case MessageTypes.ACCESS_REDACTED:
            redacted(
                f_type, f_id,
                msg_data['file_classification'],
                msg_data['usr_clearance']
            )

        case MessageTypes.ACCESS_GRANTED:
            granted(f_type, f_id)

            files = msg_data['files']

            match msg_data['f_type']:
                case 'SCP':
                    display_scp(
                        SCP.model_validate_json(msg_data['f_model']),
                        files['desc'], files['cps'], files['addenda'],
                        console
                    )
                case 'MTF':
                    display_mtf(
                        MTF.model_validate_json(msg_data['f_model']),
                        files['mission'], console
                    )
                case 'SITE':
                    display_site(
                        Site.model_validate_json(msg_data['f_model']),
                        files['loc'], files['desc'],
                        {'dossier': files['dossier']}, console
                    )
                case 'USER':
                    display_user(
                        User.model_validate_json(msg_data['f_model']),
                        console
                    )
                case _:
                    invalid_response()

        case _:
            invalid_response()



#  === Exports ===

__all__ = ['access']
