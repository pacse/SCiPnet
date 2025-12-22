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

from .models import AuditLog, IDandName, MTF, SCP, SCPColours, Site, User, \
                    get_scp_colours


class Models:
    AuditLog = AuditLog
    MTF = MTF
    SCP = SCP
    SCPColours = SCPColours
    Site = Site
    User = User

    IDandName = IDandName


__all__ = ['Models', 'get_scp_colours']

