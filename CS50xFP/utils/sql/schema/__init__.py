"""
Database schema definitions (SQLAlchemy ORM models)

Contains
--------
- Base
- validate_model
- validate_table

- MainModels
    - User
    - SCP
    - MTF
    - Site
    - AuditLog

- HelperModels
    - ClearanceLvl

    - ContainmentClass
    - SecondaryClass
    - DisruptionClass
    - RiskClass

    - Title
"""

from .base import ORMBase, validate_model, validate_table
from .helpers import ClearanceLvl, ContainmentClass, SecondaryClass, \
                     Title, DisruptionClass, RiskClass
from .main import User, SCP, MTF, Site, AuditLog



# === Exports ===

class MainModels:
    User = User
    SCP = SCP
    MTF = MTF
    Site = Site
    AuditLog = AuditLog

class HelperModels:
    ClearanceLvl = ClearanceLvl

    ContainmentClass = ContainmentClass
    SecondaryClass = SecondaryClass
    DisruptionClass = DisruptionClass
    RiskClass = RiskClass

    Title = Title


__all__ = [
           'ORMBase',
           'validate_model',
           'validate_table',

           'MainModels',
           'HelperModels'
          ]
