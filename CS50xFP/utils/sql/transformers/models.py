"""
Pydantic BaseModels to transform SQLAlchemy ORM models
into user-relevant data structures

Contains
--------
- User
- Site
- MTF
- SCP
- AuditLog
"""


from datetime import datetime
from typing import Callable, Any

from pydantic import BaseModel as Base, IPvAnyAddress, computed_field

from .formatters import FormatIDs, FormatNames
from ...general.sql_config import EXPUNGED, NONE_STR
from ...general.display_config import Styles



# === Mixins & Helpers ===

class FromAttributesMixin(Base):
    """
    Mixin to allow generation from SQLAlchemy models
    """
    model_config = {
        'from_attributes': True
    }


# helpers
class PydanticBase(FromAttributesMixin):
    """
    BaseModel for all ORM models

    Parameters
    ----------
    id : int
        the unique identifier for the model
    created_at : datetime
        timestamp of when the row was created in the sql db
    updated_at : datetime
        timestamp of when the row was last updated  in the sql db
    """

    id: int
    created_at: datetime
    updated_at: datetime

class IDandName(FromAttributesMixin):
    """
    BaseModel to store an id & name pair

    Parameters
    ----------
    id : int
        the unique identifier
    name : str
        the name associated with the id
    """
    id: int
    name: str


def computed_property(func: Callable[..., Any]) -> property:
    """
    Decorator to shorten @computed_field + @property usage
    """
    return computed_field(property(func))



# === ORM Models ===

class AuditLog(PydanticBase):
    """
    Basemodel to store audit log information

    Parameters
    ----------
    id : int
        the unique identifier for the audit log entry
    created_at : datetime
        timestamp of when the audit log row was created in the sql db
    updated_at : datetime
        timestamp of when the audit log row was last updated in the sql db

    user : User
        the user who performed the action
    user_ip : IPvAnyAddress
        the IP address of the user
    action : str
        the action performed by the user
    details : str
        additional details about the action
    status : bool
        success or failure of the action

    Properties
    ----------
    display_user : str
        the display name of the user who performed the action
    """
    user: "User"
    user_ip: IPvAnyAddress

    action: str
    details: str
    status: bool # success or failure


    @computed_property
    def display_user(self) -> str:
        """
        The display name of the user in the format
            `f'{user_name} (ID\\: {user_id:03d})'`
        """
        return FormatNames.user(
            self.user.title.name,
            self.user.name,
            self.user.id
        )


class User(PydanticBase):
    """
    BaseModel to store user information

    Parameters
    ----------
    id : int
        the unique identifier for the user
    created_at : datetime
        timestamp of when the user row was created in the sql db
    updated_at : datetime
        timestamp of when the user row was last updated in the sql db

    name : str
        the name of the user
    clearance_lvl : IDandName
        the clearance level of the user
    title : IDandName
        the title of the user
    site_id : int
        the id of the site the user is assigned to
    mtf_id : int | None = None
        the id of the MTF the user is assigned to, if any
    is_active : bool = False
        whether the user is active in the SCiPnet system
    last_login : datetime | None = None
        the last login time of the user, if any

    Properties
    ----------
    display_name : str
        the display name of the user
    display_site : str
        the display site name of the user
    display_clearance : str
        the display clearance level of the user
    """

    name: str

    clearance_lvl: IDandName
    title: IDandName

    site_id: int # only id bc names can be long (150+ chars)
    mtf_id: int | None = None

    is_active: bool = False
    last_login: datetime | None = None


    @computed_property
    def display_name(self) -> str:
        """
        The display name of the user in the format
            `f'{self.title.name} {self.name} (ID\\: {self.id})'`
        """
        return FormatNames.user(self.title.name, self.name, self.id)

    @computed_property
    def display_site(self) -> str:
        """
        The display site name of the user in the format
            `f'{site_name} (ID\\: {self.site_id:03d})'`
            (Colons are escaped for Rich md rendering)
        """
        return FormatIDs.site(self.site_id)

    @computed_property
    def display_clearance(self) -> str:
        """
        The display clearance level of the user
        """
        return self.clearance_lvl.name

    @computed_property
    def display_active(self) -> str:
        """
        The display active status of the user
            ('Active' if True, 'Inactive' if False)
        """
        return 'Active' if self.is_active else 'Inactive'


class Site(PydanticBase):
    """
    BaseModel to store site information

    Parameters
    ----------
    id : int
        the unique identifier for the site
    created_at : datetime
        timestamp of when the site row was created in the sql db
    updated_at : datetime
        timestamp of when the site row was last updated in the sql db

    name : str
        the name of the site
    director : User | None = None
        the director of the site, if any
    staff : list[User]
        list of users who are staff at the site
    scps : list[SCP]
        list of SCPs contained at the site
    mtfs : list[MTF]
        list of MTFs assigned to the site

    Properties
    ----------
    display_name : str
        the display name of the site
    display_director : str
        the display name of the site's director
    """

    name: str
    director: "User | None" = None

    staff: list["User"]
    scps: list["SCP"]
    mtfs: list["MTF"]


    @computed_property
    def display_name(self) -> str:
        """
        The display name of the site in the format
            `f'{self.name} (ID\\: {self.id:03d})'`
            (Colons are escaped for Rich md rendering)
        """
        return FormatNames.site(self.name, self.id)

    @computed_property
    def display_director(self) -> str:
        """
        The display name of the site's director in the format
            `f'{director_title} {director_name} (ID\\: {director_id})'`
            (Colons are escaped for Rich md rendering)
            or `EXPUNGED` if None
        """
        if self.director:
            return FormatNames.user(
                self.director.title.name,
                self.director.name,
                self.director.id
            )
        return EXPUNGED


class MTF(PydanticBase):
    """
    BaseModel to store MTF information

    Parameters
    ----------
    id : int
        the unique identifier for the MTF
    created_at : datetime
        timestamp of when the MTF row was created in the sql db
    updated_at : datetime
        timestamp of when the MTF row was last updated in the sql db

    name : str
        the name of the MTF
    nickname : str
        the nickname of the MTF
    leader : User | None = None
        the leader of the MTF, if any
    site : Site | None = None
        the site the MTF is assigned to, if any
    active : bool = True
        whether the MTF is active
    scps : list[SCP]
        list of SCPs assigned to the MTF
    members : list[User]
        list of users who are members of the MTF

    Properties
    ----------
    display_name : str
        the display name of the MTF
    display_nickname : str
        the display nickname of the MTF
    display_site : str
        the display site name of the MTF
    display_leader : str
        the display name of the MTF's leader
    """

    name: str
    nickname: str
    leader: "User | None" = None
    site: "Site | None" = None
    active: bool = True

    scps: list["SCP"]
    members: list["User"]


    @computed_property
    def display_name(self) -> str:
        """
        The display name of the MTF in the format
            `f'MTF {self.name} (ID\\: {self.id})'`
            (Colons are escaped for Rich md rendering)
        """
        return FormatNames.mtf(self.name, self.id)

    @computed_property
    def display_nickname(self) -> str:
        """
        The display nickname of the MTF in the format
            `f'"{self.nickname}"'`
        """
        return f'"{self.nickname}"'

    @computed_property
    def display_site(self) -> str:
        """
        The display site name of the MTF in the format
            `f'{site_name} (ID\\: {site_id:03d})'`
            (Colons are escaped for Rich md rendering)
            or `EXPUNGED` if None
        """
        if self.site:
            return FormatIDs.site(self.site.id)
        return EXPUNGED

    @computed_property
    def display_leader(self) -> str:
        """
        The display name of the MTF's leader in the format
            `f'{leader_title} {leader_name} (ID\\: {leader_id})'`
            (Colons are escaped for Rich md rendering)
            or `EXPUNGED` if None
        """
        if self.leader:
            return FormatNames.user(
                self.leader.title.name,
                self.leader.name,
                self.leader.id
            )
        return EXPUNGED

    @computed_property
    def display_active(self) -> str:
        """
        The display active status of the MTF
            ('Active' if True, 'Inactive' if False)
        """
        return 'Active' if self.active else 'Inactive'

"""
TODO: add MTF subtypes: (After submit final project)
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


class SCP(PydanticBase):
    """
    BaseModel to store SCP information

    Parameters
    ----------
    id : int
        the unique identifier for the SCP
    created_at : datetime
        timestamp of when the SCP row was created in the sql db
    updated_at : datetime
        timestamp of when the SCP row was last updated in the sql db

    name : str
        the codename of the SCP
    clearance_lvl : IDandName
        the clearance level required to access the SCP
    containment_class : IDandName
        the containment class of the SCP
    secondary_class : IDandName | None = None
        the secondary containment class of the SCP, if any
    disruption_class : IDandName | None = None
        the disruption class of the SCP, if any
    risk_class : IDandName | None = None
        the risk class of the SCP, if any
    site_responsible_id : int | None = None
        the id of the site responsible for the SCP, if any
    mtf : MTF | None = None
        the MTF assigned to the SCP, if any

    Properties
    ----------
    display_id : str
        the display ID of the SCP in the format
        `f'SCP-{self.id:03d}'`
    display_name : str
        the display name of the SCP in the format
        `f'"{self.name}"'`
    display_clearance : str
        the display clearance level of the SCP
    display_containment : str
        the display containment class of the SCP
    display_secondary : str
        the display secondary containment class of the SCP,
        or `EXPUNGED` if none
    display_disruption : str
        the display disruption class of the SCP,
        or `EXPUNGED` if none
    display_risk : str
        the display risk class of the SCP,
        or `EXPUNGED` if none
    display_site : str
        the display site responsible for the SCP in the format
        `f'Site-{self.site_responsible_id:03d}'`,
        or `EXPUNGED` if none
    display_mtf : str
        the display MTF assigned to the SCP in the format
        `f'{mtf_name} (ID\\: {mtf_id})'`,
        or `EXPUNGED` if none
    """

    name: str # SCP codename, eg. 'The "Living" Room' (002)
    clearance_lvl: IDandName

    containment_class: IDandName
    secondary_class: IDandName | None = None

    disruption_class: IDandName | None = None
    risk_class: IDandName | None = None

    site_responsible_id: int | None = None
    mtf: "MTF | None" = None


    @computed_property
    def display_id(self) -> str:
        """
        The display ID of the SCP in the format
            `f'SCP-{self.id:03d}'`
        """
        return FormatIDs.scp(self.id)

    @computed_property
    def display_name(self) -> str:
        """
        The display name of the SCP in the format
            `f'"{self.name}"'`
        """
        return f'"{self.name}"'

    @computed_property
    def display_clearance(self) -> str:
        """
        The display clearance level of the SCP
        """
        return self.clearance_lvl.name

    @computed_property
    def display_containment(self) -> str:
        """
        The display containment class of the SCP
        """
        return self.containment_class.name

    @computed_property
    def display_secondary(self) -> str:
        """
        The display secondary containment class of the SCP,
        or `EXPUNGED` if none
        """
        if self.secondary_class:
            return self.secondary_class.name
        return NONE_STR

    @computed_property
    def display_disruption(self) -> str:
        """
        The display disruption class of the SCP,
        or `EXPUNGED` if none
        """
        if self.disruption_class:
            return self.disruption_class.name
        return EXPUNGED

    @computed_property
    def display_risk(self) -> str:
        """
        The display risk class of the SCP,
        or `EXPUNGED` if none
        """
        if self.risk_class:
            return self.risk_class.name
        return EXPUNGED

    @computed_property
    def display_site(self) -> str:
        """
        The display site responsible for the SCP in the format:
            `f'Site-{self.site_responsible_id:03d}'`
        or `EXPUNGED` if none
        """
        if self.site_responsible_id:
            return FormatIDs.site(self.site_responsible_id)
        return EXPUNGED

    @computed_property
    def display_mtf(self) -> str:
        """
        The display MTF assigned to the SCP in the format:
            `f'{mtf_name} (ID\\: {mtf_id})'`
        or `NONE_STR` if none
        """
        if self.mtf:
            return FormatNames.mtf(
                                   self.mtf.name,
                                   self.mtf.id,
                                   self.mtf.nickname
                                  )
        return NONE_STR


class SCPColours(Base):
    """
    BaseModel to store hex colour codes and rich styles
    for the display of an SCP

    Parameters
    ----------
    clear_lvl : str
        the clearance level colour code
    cont_class : str
        the containment class colour code
    disrupt_class : str | None
        the disruption class colour code, if any
    risk_class : str | None
        the risk class colour code, if any
    """

    clear_lvl: str
    cont_class: str
    scnd_class: str | None
    disrupt_class: str | None
    risk_class: str | None

def get_scp_colours(scp: SCP) -> SCPColours:
    """
    Generates an SCPColours object from an SCP object

    Parameters
    ----------
    scp : SCP
        the SCP object to generate colours for

    Returns
    -------
    SCPColours
        the generated SCPColours object
    """
    clear_lvl = Styles.CLEAR_LVL[scp.clearance_lvl.id]
    cont_class = Styles.CONT_CLASS[scp.containment_class.name]
    if scp.secondary_class:
        scnd_class = Styles.CONT_CLASS[scp.secondary_class.name]
    else:
        scnd_class = Styles.OTHER_CONT_CLASS
    if scp.disruption_class:
        disrupt_class = Styles.CLEAR_LVL[scp.disruption_class.id]
    else:
        disrupt_class = None
    if scp.risk_class:
        risk_class = Styles.CLEAR_LVL[scp.risk_class.id]
    else:
        risk_class = None

    return SCPColours(
        clear_lvl=clear_lvl,
        cont_class=cont_class,
        scnd_class=scnd_class,
        disrupt_class=disrupt_class,
        risk_class=risk_class
    )



# Resolve forward references (Pointed out by Copilot)
User.model_rebuild()
Site.model_rebuild()
MTF.model_rebuild()
SCP.model_rebuild()
AuditLog.model_rebuild()



# === Exports ===

__all__ = [
           # Models
           'User',
           'Site',
           'MTF',
           'SCP',
           'SCPColours',
           'AuditLog',

           # Other
           'get_scp_colours',
           'IDandName'
          ]
