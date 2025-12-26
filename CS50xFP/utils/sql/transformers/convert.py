"""
Logic to convert from SQLAlchemy to Pydantic models
"""

from typing import overload

from . import Models as PydanticModels
from .models import PydanticBase

from ...sql.schema import MainModels as ORMModels
from ...sql.schema import ORMBase


# === Helper consts ===

ORM_TO_PYDANTIC_MAP: dict[type[ORMBase], type[PydanticBase]] = {
    ORMModels.User: PydanticModels.User,
    ORMModels.SCP: PydanticModels.SCP,
    ORMModels.MTF: PydanticModels.MTF,
    ORMModels.Site: PydanticModels.Site,
    ORMModels.AuditLog: PydanticModels.AuditLog
}



# === Main Func ===

@overload
def orm_to_pydantic(orm_obj: ORMModels.User) -> PydanticModels.User: ...
@overload
def orm_to_pydantic(orm_obj: ORMModels.SCP) -> PydanticModels.SCP: ...
@overload
def orm_to_pydantic(orm_obj: ORMModels.MTF) -> PydanticModels.MTF: ...
@overload
def orm_to_pydantic(orm_obj: ORMModels.Site) -> PydanticModels.Site: ...
@overload
def orm_to_pydantic(orm_obj: ORMModels.AuditLog) -> PydanticModels.AuditLog: ...

def orm_to_pydantic(orm_obj: ORMBase) -> PydanticBase:
    """
    Converts an ORM object to a Pydantic object

    Parameters
    ----------
    orm_obj : ORMBase
        The ORM object to convert

    Returns
    -------
    PydanticBase
        The converted Pydantic object

    Raises
    ------
    ValueError
        If no corresponding Pydantic model exists for `orm_obj`'s type
    """

    orm_type = type(orm_obj)

    if orm_type not in ORM_TO_PYDANTIC_MAP:
        raise ValueError(f"No Pydantic model for {orm_type.__name__}")

    return ORM_TO_PYDANTIC_MAP[orm_type].model_validate(orm_obj)
