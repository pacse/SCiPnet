"""
Basic server functions

Contains
--------
- auth_usr(user_id: int, password: str) -> tuple[bool, PydanticModels.User | None]
"""

from werkzeug.security import check_password_hash

from ..general.server_config import Server
from ..general.validation import validate_int, validate_str


from ..sql.queries import get_model, db_session
from ..sql.transformers import Models as PydanticModels, orm_to_pydantic
from ..sql.schema import MainModels as ORMModels


def auth_usr(
             user_id: int,
             password: str  # (TODO: Expect hashed password after FP submission)
            ) -> tuple[str, None] | tuple[None, PydanticModels.User]:
    """
    Authenticates a user

    Parameters
    ----------
    user_id : int
        The user's ID
    password : str
        The password to authenticate

    Returns
    -------
    tuple[str, None]
        The invalid field if authentication failed, None

    tuple[None, PydanticModels.User]
        None and the Pydantic User model if authentication succeeded

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

    with db_session() as session:
        user = session.get(ORMModels.User, user_id)

        if not user:
            if Server.DEBUG:
                print('Failure, returning: user_id, None')
            return 'user_id', None

        if not check_password_hash(str(user.password), password):
            if Server.DEBUG:
                print('Failure, returning: password, None')
            return 'password', None

        else:
            if Server.DEBUG:
                print(f'Success, returning: True, {user!r}')
            return None, orm_to_pydantic(user)


__all__ = ['auth_usr']
