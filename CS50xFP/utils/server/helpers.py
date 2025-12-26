"""
Helpers for server operations

Contains
--------
- auth_usr(id: int, password: str) -> tuple[bool, dict[str, Any] | None]
"""

from typing import Any
from werkzeug.security import check_password_hash

from ..general.server_config import Server
from ..general.validation import validate_int, validate_str

from ..sql.queries import get_model
from ..sql.transformers import Models as PydanticModels, orm_to_pydantic
from ..sql.schema import MainModels as ORMModels


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
        print(f'Authenticating user {user_id!r} with password: {password!r}')

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
