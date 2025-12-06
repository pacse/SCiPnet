"""
BaseModels to store used information
(by client) provided by the deepwell
"""
from pydantic import IPvAnyAddress, BaseModel as Base
from datetime import datetime

class FromAttributesMixin(Base):
    """
    Mixin to allow generation from SQLAlchemy models
    """
    model_config = {
        'from_attributes': True
    }

# helpers
class ORMBase(FromAttributesMixin):
    """
    BaseModel for all ORM models

    All models have an id, created_at, and updated_at
    """

    id: int
    created_at: datetime
    updated_at: datetime


class IDandName(FromAttributesMixin):
    """
    BaseModel to store an id and name pair
    """
    id: int
    name: str


# models
class User(ORMBase):
    """
    BaseModel to store user information
    """
    name: str

    clearance_lvl: IDandName
    title: IDandName

    site_id: int # only id bc names can be long (150+ chars)
    mtf: "MTF | None" = None

    is_active: bool = False
    last_login: datetime | None = None


class Site(ORMBase):
    name: str
    director: "User | None" = None

    staff: list["User"]
    scps: list["SCP"]
    mtfs: list["MTF"]


class MTF(ORMBase):
    name: str
    nickname: str
    leader: "User | None" = None
    site: "Site | None" = None
    active: bool = True

    scps: list["SCP"]
    members: list["User"]

"""
TODO: add MTF subtypes: (Do after submit final project)
Anomaly Response Command (ARC): Commands ARC teams
    Mobile Task Force (MTF): General-purpose Force
    Naval Task Force (NTF): Force specializing in naval operations
    Rapid Response Team (RRT): Team for rapid deployment to incidents
    Tactical Response Team (TRT): Team for tactical operations
    Special Operations Group (SOG): Elite special operations unit

Team vs Force:
    Team: Smaller, specialized unit within a Force
    Force: Heavier, more general-purpose unit

    Eg, when a 'MTF' is sent into an SCP, it's
    actually a Team from that MTF

"""


class SCPColours(Base):
    """
    BaseModel to store hex colour
    codes for the display of an SCP
    """
    class_lvl: str
    cont_clss: str
    disrupt_clss: str | None
    rsk_clss: str | None


class SCP(ORMBase):
    """
    A dataclass to store a SCP's information
    after getting its data from the deepwell
    """
    name: str # SCP codename, eg 'The "Living" Room' (002)
    clearance_lvl: IDandName

    containment_class: IDandName
    secondary_class: IDandName | None = None

    disruption_class: IDandName | None = None
    risk_class: IDandName | None = None

    site_responsible_id: int | None = None
    mtf: "MTF | None" = None

class AuditLog(ORMBase):
    """
    A dataclass to store an audit log's information
    after getting its data from the deepwell
    """
    user: "User"
    user_ip: IPvAnyAddress

    action: str
    details: str
    status: bool # success or failure


# Resolve forward references (Pointed out by Copilot)
User.model_rebuild()
Site.model_rebuild()
MTF.model_rebuild()
SCP.model_rebuild()
AuditLog.model_rebuild()


# namespace
class Models:
    User = User
    Site = Site
    MTF = MTF
    SCP = SCP
    AuditLog = AuditLog

    IDandName = IDandName

    SCPColours = SCPColours
