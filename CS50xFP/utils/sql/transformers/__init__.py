"""
Pydantic models for SQL data transformation.

Takes raw SQL data and transforms it into structured Pydantic models
for easier manipulation. All models have display properties to handle
null values.

Contains
--------
- Models
    - AuditLog
    - MTF
    - SCP
    - Site
    - User

    - IDandName
- get_scp_colours
"""

from .models import PydanticBase, AuditLog, IDandName, MTF, SCP, \
                    SCPColours, Site, User, get_scp_colours, UserRef, \
                    SiteRef, MTFRef, SCPRef


# Define Models class BEFORE importing convert to avoid circular import
class Models:
    AuditLog = AuditLog
    MTF = MTF
    SCP = SCP
    SCPColours = SCPColours
    Site = Site
    User = User

    IDandName = IDandName

class RefModels:
    MTF = MTFRef
    SCP = SCPRef
    Site = SiteRef
    User = UserRef


# Import convert AFTER Models is defined to avoid circular import
from .convert import orm_to_pydantic


__all__ = [
           'PydanticBase',
           'orm_to_pydantic',
           'Models',
           'get_scp_colours'
          ]

