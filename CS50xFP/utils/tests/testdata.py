"""
Test fixtures for bar rendering tests
Provides sample data for SCP, Site, MTF, and User bars
"""

from utils.sql.transformers import Models
from datetime import datetime

# === Helper IDandName instances ===

# Clearance Levels
CLEARANCES: list[Models.IDandName] = [
    Models.IDandName(id=0, name="NULL"),  # Placeholder for 0 index
    Models.IDandName(id=1, name="Level 1 - Unrestricted"),
    Models.IDandName(id=2, name="Level 2 - Restricted"),
    Models.IDandName(id=3, name="Level 3 - Confidential"),
    Models.IDandName(id=4, name="Level 4 - Secret"),
    Models.IDandName(id=5, name="Level 5 - Top Secret"),
    Models.IDandName(id=6, name="Level 6 - COSMIC Top Secret"),
]

# Titles
TITLE_RESEARCHER = Models.IDandName(id=1, name="Researcher")
TITLE_SENIOR_RESEARCHER = Models.IDandName(id=2, name="Senior Researcher")
TITLE_DIRECTOR = Models.IDandName(id=3, name="Site Director")
TITLE_O5 = Models.IDandName(id=4, name="O5 Council Member")
TITLE_ADMINISTRATOR = Models.IDandName(id=5, name="The Administrator")

# Containment Classes
CONT_SAFE = Models.IDandName(id=1, name="Safe")
CONT_EUCLID = Models.IDandName(id=2, name="Euclid")
CONT_KETER = Models.IDandName(id=3, name="Keter")
CONT_ESOTERIC = Models.IDandName(id=4, name="Esoteric")

# Secondary Classes
SEC_NONE = None
SEC_NEUTRALIZED = Models.IDandName(id=1, name="Neutralized")
SEC_EXPLAINED = Models.IDandName(id=2, name="Explained")
SEC_THAUMIEL = Models.IDandName(id=4, name="Thaumiel")

# Disruption Classes
DISRUPTS: list[Models.IDandName] = [
    Models.IDandName(id=0, name="NULL"),  # Placeholder for 0 index
    Models.IDandName(id=1, name="Level 1 - Dark"),
    Models.IDandName(id=2, name="Level 2 - Vlam"),
    Models.IDandName(id=3, name="Level 3 - Keneq"),
    Models.IDandName(id=4, name="Level 4 - Ekhi"),
    Models.IDandName(id=5, name="Level 5 - Amida"),
]

# Risk Classes
RISKS: list[Models.IDandName] = [
    Models.IDandName(id=0, name="NULL"),  # Placeholder for 0 index
    Models.IDandName(id=1, name="Level 1 - Notice"),
    Models.IDandName(id=2, name="Level 2 - Caution"),
    Models.IDandName(id=3, name="Level 3 - Warning"),
    Models.IDandName(id=4, name="Level 4 - Danger"),
    Models.IDandName(id=5, name="Level 5 - Critical"),
]



# === Test Users ===

def create_test_user(
    user_id: int = 1001,
    name: str = "Dr. John Smith",
    clearance: Models.IDandName = CLEARANCES[3],
    title: Models.IDandName = TITLE_RESEARCHER,
    site_id: int = 19,
    mtf_id: int | None = None,
    is_active: bool = True
) -> Models.User:

    """Create a test user with customizable parameters"""
    return Models.User(
        id=user_id,
        name=name,
        clearance_lvl=clearance,
        title=title,
        site_id=site_id,
        mtf_id=mtf_id,
        is_active=is_active,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )


TEST_RESEARCHER = create_test_user(
    user_id=1001,
    name="Dr. Sarah Chen",
    clearance=CLEARANCES[6],
    title=TITLE_RESEARCHER,
    site_id=19
)

TEST_SENIOR_RESEARCHER = create_test_user(
    user_id=1002,
    name="Dr. Marcus Rodriguez",
    clearance=CLEARANCES[3],
    title=TITLE_SENIOR_RESEARCHER,
    site_id=19
)

TEST_DIRECTOR = create_test_user(
    user_id=1003,
    name="Dr. Emily Watson",
    clearance=CLEARANCES[4],
    title=TITLE_DIRECTOR,
    site_id=19
)

TEST_O5 = create_test_user(
    user_id=1,
    name="O5-7",
    clearance=CLEARANCES[5],
    title=TITLE_O5,
    site_id=1
)

TEST_ADMINISTRATOR = create_test_user(
    user_id=0,
    name="", # The Administrator does not have a name
    clearance=CLEARANCES[5],
    title=TITLE_ADMINISTRATOR,
    site_id=0
)

TEST_USERS = [
    TEST_RESEARCHER,
    TEST_SENIOR_RESEARCHER,
    TEST_DIRECTOR,
    TEST_O5,
    TEST_ADMINISTRATOR
]



# === Test Sites ===

def create_test_site(
    site_id: int = 19,
    name: str = "Site-19",
    director: Models.User | None = None
) -> Models.Site:

    """Create a test site with customizable parameters"""
    return Models.Site(
        id=site_id,
        name=name,
        director=director,
        staff=[],
        scps=[],
        mtfs=[],
        created_at=datetime.now(),
        updated_at=datetime.now()
    )


TEST_SITE_19 = create_test_site(
    site_id=19,
    name="Site-19",
    director=TEST_DIRECTOR
)

TEST_SITE_17 = create_test_site(
    site_id=17,
    name="Armed Reliquary and Containment Area-17"
)

TEST_SITE_01 = create_test_site(
    site_id=1,
    name="Site-01",
    director=TEST_O5
)


TEST_SITES = [
    TEST_SITE_19,
    TEST_SITE_17,
    #TEST_SITE_01
]



# === Test MTFs ===

def create_test_mtf(
    mtf_id: int = 1,
    name: str = "Alpha-1",
    nickname: str = "Red Right Hand",
    leader: Models.User | None = None,
    site: "Models.Site | None" = None,
    active: bool = True
) -> Models.MTF:

    """Create a test MTF with customizable parameters"""
    return Models.MTF(
        id=mtf_id,
        name=name,
        nickname=nickname,
        leader=leader,
        site=site,
        active=active,
        scps=[],
        members=[],
        created_at=datetime.now(),
        updated_at=datetime.now()
    )


TEST_MTF_ALPHA1 = create_test_mtf(
    mtf_id=1,
    name="Alpha-1",
    nickname="Red Right Hand",
    active=True
)

TEST_MTF_OMEGA7 = create_test_mtf(
    mtf_id=74,
    name="Omega-7",
    nickname="Pandora's Box",
    leader=TEST_DIRECTOR,
    site=TEST_SITE_19,
    active=False
)

TEST_MTF_ETA10 = create_test_mtf(
    mtf_id=75,
    name="Eta-10",
    nickname="See No Evil",
    active=True
)


TEST_MTFS = [
    TEST_MTF_ALPHA1,
    TEST_MTF_OMEGA7,
    TEST_MTF_ETA10
]



# === Test SCPs ===

def create_test_scp(
    scp_id: int = 173,
    name: str = "The Sculpture",
    clearance: Models.IDandName = CLEARANCES[2],

    containment_class: Models.IDandName = CONT_EUCLID,
    secondary_class: Models.IDandName | None = None,

    disruption_class: Models.IDandName | None = None,
    risk_class: Models.IDandName | None = None,

    site_responsible_id: int | None = None,
    mtf: Models.MTF | None = None
) -> Models.SCP:

    """Create a test SCP with customizable parameters"""
    return Models.SCP(
        id=scp_id,
        name=name,
        clearance_lvl=clearance,

        containment_class=containment_class,
        secondary_class=secondary_class,

        disruption_class=disruption_class,
        risk_class=risk_class,

        site_responsible_id=site_responsible_id,
        mtf=mtf,

        created_at=datetime.now(),
        updated_at=datetime.now()
    )


TEST_SCP_173 = create_test_scp(
    scp_id=173,
    name="The Sculpture",
    clearance=CLEARANCES[6],
    containment_class=CONT_EUCLID,
    disruption_class=DISRUPTS[1],
    risk_class=RISKS[5],
    site_responsible_id=19,
    mtf=TEST_MTF_ETA10
)

TEST_SCP_682 = create_test_scp(
    scp_id=682,
    name="Hard-to-Destroy Reptile",
    clearance=CLEARANCES[5],
    containment_class=CONT_KETER,
    disruption_class=DISRUPTS[2],
    risk_class=RISKS[1],
    site_responsible_id=19,
    mtf=TEST_MTF_OMEGA7
)

TEST_SCP_999 = create_test_scp(
    scp_id=999,
    name="The Tickle Monster",
    clearance=CLEARANCES[4],
    containment_class=CONT_SAFE,
    disruption_class=DISRUPTS[3],
    risk_class=RISKS[3],
    site_responsible_id=19,
    mtf=None
)

TEST_SCP_2000 = create_test_scp(
    scp_id=2000,
    name="Deus Ex Machina",
    clearance=CLEARANCES[3],
    containment_class=CONT_ESOTERIC,
    secondary_class=None,
    disruption_class=None,  # Expunged
    risk_class=None,  # Expunged
    site_responsible_id=None,  # Expunged
    mtf=None
)

TEST_SCP_5000 = create_test_scp(
    scp_id=5000,
    name="Why?",
    clearance=CLEARANCES[2],
    containment_class=CONT_SAFE,
    secondary_class=SEC_NEUTRALIZED,
    disruption_class=DISRUPTS[4],
    risk_class=RISKS[1],
    site_responsible_id=17
)

TEST_SCPS = [
    TEST_SCP_173,
    TEST_SCP_682,
    TEST_SCP_999,
    TEST_SCP_2000,
    TEST_SCP_5000
]


# === Aggregate Test Data ===
class TestData:
    """Aggregate test data for easy access"""

    USERS = TEST_USERS
    MTFS = TEST_MTFS
    SITES = TEST_SITES
    SCPS = TEST_SCPS
