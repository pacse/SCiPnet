"""
Helper DB table definitions

Contains
--------
- User related
    - ClearanceLvl
    - Title

- SCP related
    - ContainmentClass
    - SecondaryClass
    - DisruptionClass
    - RiskClass

Notes
-----
All helper tables have:
- id (primary key)
- name (50 chars max, indexed)
- created_at, updated_at (timestamps)
"""


from .base import ORMBase, HelperTableMixin, rel

from sqlalchemy.orm import Mapped
from typing import TYPE_CHECKING

if TYPE_CHECKING: # avoid circular imports for type hinting
    from .main import User, SCP



# === User related tables ===
class ClearanceLvl(HelperTableMixin, ORMBase):
    __tablename__ = 'clearance_lvls'

    users: Mapped[list['User']] = rel('clearance_lvl')
    scps: Mapped[list['SCP']] = rel('clearance_lvl')


class Title(HelperTableMixin, ORMBase):
    __tablename__ = 'titles'

    users: Mapped[list['User']] = rel('title')


# SCP specific models
class ContainmentClass(HelperTableMixin, ORMBase):
    __tablename__ = 'containment_classes'

    scps: Mapped[list['SCP']] = rel('containment_class')


class SecondaryClass(HelperTableMixin, ORMBase):
    __tablename__ = 'secondary_classes'

    scps: Mapped[list['SCP']] = rel('secondary_class')


class DisruptionClass(HelperTableMixin, ORMBase):
    __tablename__ = 'disruption_classes'

    scps: Mapped[list['SCP']] = rel('disruption_class')


class RiskClass(HelperTableMixin, ORMBase):
    __tablename__ = 'risk_classes'

    scps: Mapped[list['SCP']] = rel('risk_class')



# === Exports ===
__all__ = [
           # User related
           'ClearanceLvl',
           'Title',

           # SCP related
           'ContainmentClass',
           'SecondaryClass',
           'DisruptionClass',
           'RiskClass'
          ]
