"""
All SQLAlchemy table definitions for
SCiPnet.db and related table information/funcs
"""

from sqlalchemy import (Column, Integer, String, Boolean,
                        DateTime, ForeignKey, Index)

from sqlalchemy.orm import (relationship, DeclarativeBase,
                            validates, Mapped)

from datetime import datetime

# for validation
import re, ipaddress

WK_HASH_REGEX = r'scrypt:32768:8:1\$[A-Za-z0-9]{16}\$[A-Za-z0-9]{128}'
"""werkzeug hash regex for validation"""


# ease of life shortenings
def col_int_pk() -> Column[int]:
    """
    Returns a primary key integer column with autoincrement.
    """
    return Column(Integer, primary_key=True, autoincrement=True)

def col_int_fk(ref: str, nullable=False) -> Column[int]:
    """
    Returns a foreign key integer column.

    ref: `<table_name>.<column_name>`
    """
    return Column(Integer, ForeignKey(ref), nullable=nullable)


def col_str(length: int, nullable=True) -> Column[str]:
    """
    Returns a string column.
    """
    return Column(String(length), nullable=nullable)


def wk_hash(nullable: bool) -> Column[str]:
    """
    Returns a string column for storing a werkzeug password hash.
    """
    return col_str(162, nullable) # 162 is max length of werkzeug hash


def rel(to: str,
        /, back_pop: str, # '/,' forces kwargs after
        keys: list | None = None
       ) -> Mapped:
    """
    Returns a relationship to another table.
    """
    return relationship(to,
                        back_populates=back_pop, foreign_keys=keys)


# ease of life Mixin
class HelperTableMixin:
    """
    Mixin that adds a 50 char `name` column.
    """
    name = col_str(50, False)


# base class for all tables
class Base(DeclarativeBase):
    """
    all tables have:
        `id`: primary key column
        `created_at`: when row was created | default: current timestamp
        `updated_at`: when row was last updated | default: current timestamp
    """
    id = col_int_pk()

    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now,
                        onupdate=datetime.now, nullable=False)



# === Main Models ===

class User(Base):
    __tablename__ = 'users'


    name = col_str(50, nullable = False)
    password = wk_hash(nullable = False)
    override_phrase = wk_hash(nullable = True)

    clearance_lvl_id = col_int_fk('clearance_lvls.id', nullable = False)

    title_id = col_int_fk('titles.id', nullable = False)
    site_id = col_int_fk('sites.id', nullable = False)
    mtf_id = col_int_fk('mtfs.id', nullable = True)

    is_active = Column(Boolean, default = False, nullable = False)
    last_login = Column(DateTime, default = None, nullable = True)

    # relationships

    # local
    clearance_lvl: Mapped["ClearanceLvl"] = rel('ClearanceLvl', back_pop='users')
    title: Mapped["Title"] = rel('Title', back_pop='users')
    site: Mapped["Site"] = rel('Site', back_pop='staff', keys=[site_id])
    mtf: Mapped["MTF | None"] = rel('MTF', back_pop='leader', keys=[mtf_id])

    # acknowledge other tables
    audit_logs: Mapped[list["AuditLog"]] = rel('AuditLog', back_pop='user')
    led_mtfs: Mapped[list["MTF"]] = relationship('MTF', back_populates='members', foreign_keys='MTF.leader_id')
    directed_sites: Mapped[list["Site"]] = relationship('Site', back_populates='director', foreign_keys='Site.director_id')


    # validator! 🎉
    @validates('password', 'override_phrase')
    def validate_hash(self, key, value):
        if len(value) != 162:
            raise ValueError(f'Error with {key!r}:\nWerkzeug hash must be 162 characters long')

        elif not re.fullmatch(WK_HASH_REGEX, value):
            raise ValueError(f'Error with {key!r}:\nProvided value is not a valid Werkzeug hash (correct length (162), did not match regex)')
        return value


    __table_args__ = (
        # table indexes
        Index('idx_users_name', name),
        Index('idx_users_clearance_lvl_id', clearance_lvl_id),
        Index('idx_users_site_id', site_id),
        Index('idx_users_title_id', title_id),
        Index('idx_users_is_active', is_active),
        Index('idx_users_last_login', last_login),
        Index('idx_users_created_at', 'created_at'),
        Index('idx_users_updated_at', 'updated_at')
    )

    def __repr__(self):
        return (
                f"<User(id={self.id}, name='{self.name}', "
                f"password='{self.password}', "
                f"override_phrase='{self.override_phrase}', "
                f"clearance_lvl_id={self.clearance_lvl_id}, "
                f"title_id={self.title_id}, site_id={self.site_id}, "
                f"is_active={self.is_active}, last_login={self.last_login}, "
                f"created_at={self.created_at}, updated_at={self.updated_at}"
                ")>"
               )


class SCP(Base):
    __tablename__ = 'scps'

    clearance_lvl_id = col_int_fk('clearance_lvls.id', False)

    containment_class_id = col_int_fk('containment_classes.id', False)
    secondary_class_id = col_int_fk('secondary_classes.id', True)

    disruption_class_id = col_int_fk('disruption_classes.id', True)
    risk_class_id = col_int_fk('risk_classes.id', True)

    site_responsible_id = col_int_fk('sites.id', True)
    assigned_task_force_id = col_int_fk('mtfs.id', True)

    # relationships

    # local
    clearance_lvl: Mapped["ClearanceLvl"] = rel('ClearanceLvl', back_pop='scps')

    containment_class: Mapped["ContainmentClass"] = rel('ContainmentClass', back_pop='scps')
    secondary_class: Mapped["SecondaryClass | None"] = rel('SecondaryClass', back_pop='scps')

    disruption_class: Mapped["DisruptionClass | None"] = rel('DisruptionClass', back_pop='scps')
    risk_class: Mapped["RiskClass | None"] = rel('RiskClass', back_pop='scps')

    site_responsible: Mapped["Site | None"] = rel('Site', back_pop='scps')
    mtf: Mapped["MTF | None"] = rel('MTF', back_pop='scps')



    __table_args__ = (

        # table indexes (maybe _every_ col is overkill but we ball)
        Index('idx_scps_clearance_lvl_id', clearance_lvl_id),
        Index('idx_scps_containment_class_id', containment_class_id),
        Index('idx_scps_secondary_class_id', secondary_class_id),
        Index('idx_scps_disruption_class_id', disruption_class_id),
        Index('idx_scps_risk_class_id', risk_class_id),
        Index('idx_scps_site_responsible_id', site_responsible_id),
        Index('idx_scps_assigned_task_force_id', assigned_task_force_id),
        Index('idx_scps_created_at', 'created_at'),
        Index('idx_scps_updated_at', 'updated_at')
    )


    def __repr__(self):
        return (
                f"<SCP(id={self.id}, "
                f"clearance_lvl_id={self.clearance_lvl_id}, "
                f"containment_class_id={self.containment_class_id}, "
                f"secondary_class_id={self.secondary_class_id}, "
                f"disruption_class_id={self.disruption_class_id}, "
                f"risk_class_id={self.risk_class_id}, "
                f"site_responsible_id={self.site_responsible_id}, "
                f"assigned_task_force_id={self.assigned_task_force_id}, "
                f"created_at={self.created_at}, updated_at={self.updated_at}"
                ")>"
               )


class MTF(Base):
    __tablename__ = 'mtfs'

    name = col_str(25, nullable=False) # eg. Epsilon-6
    nickname = col_str(100, nullable=False) # eg. 'Village Idiots', long just in case

    leader_id = col_int_fk('users.id', nullable=True)
    site_id = col_int_fk('sites.id', nullable=True)

    active = Column(Boolean, default=True, nullable=False)

    # relationships

    # local
    leader: Mapped["User | None"] = relationship('User', back_populates='led_mtfs', foreign_keys=[leader_id])
    site: Mapped["Site | None"] = rel('Site', back_pop='mtfs')

    # acknowledge other tables
    scps: Mapped[list["SCP"]] = rel('SCP', back_pop='mtf')
    members: Mapped[list["User"]] = relationship('User', back_populates='mtf', foreign_keys='User.mtf_id')



    __table_args__ = (
        # table indexes
        Index('idx_mtfs_name', name),
        Index('idx_mtfs_nickname', nickname),
        Index('idx_mtfs_leader_id', leader_id),
        Index('idx_mtfs_site_id', site_id),
        Index('idx_mtfs_created_at', 'created_at'),
        Index('idx_mtfs_updated_at', 'updated_at')
    )

    def __repr__(self):
        return (
                f"<MTF(id={self.id}, name='{self.name}', "
                f"nickname='{self.nickname}', leader_id={self.leader_id}, "
                f"site_id={self.site_id}, active={self.active}, "
                f"created_at={self.created_at}, updated_at={self.updated_at}"
                ")>"
               )


class Site(Base):
    __tablename__ = 'sites'

    name = col_str(100, False) # eg. 'Site-01'
    director_id = col_int_fk('users.id', True)


    # relationships

    # local
    director: Mapped["User | None"] = rel('User', back_pop='directed_sites', keys=[director_id])

    # acknowledge other tables
    scps: Mapped[list["SCP"]] = rel('SCP', back_pop='site_responsible')
    mtfs: Mapped[list["MTF"]] = rel('MTF', back_pop='site')
    staff: Mapped[list["User"]] = relationship('User', back_populates='site', foreign_keys='User.site_id')

    __table_args__ = (
        Index('idx_sites_name', name),
        Index('idx_sites_director', director_id),
        Index('idx_sites_created_at', 'created_at'),
        Index('idx_sites_updated_at', 'updated_at')
    )

    def __repr__(self):
        return (
                f"<Site(id={self.id}, name='{self.name}', "
                f"director_id={self.director_id}, "
                f"created_at={self.created_at}, updated_at={self.updated_at}"
                ")>"
               )


class AuditLog(Base):
    __tablename__ = 'audit_log'

    user_id = col_int_fk('users.id', nullable=False)
    user_ip = col_str(60, nullable=False) # IP address of the user, long enough for IPv6, i think

    action = col_str(255, nullable=False) # description of action taken
    details = col_str(255, nullable=False) # additional details about the action
    status = Column(Boolean, nullable=False) # success or failure of the action


    # acknowledge user relationship
    user: Mapped["User"] = rel('User', back_pop='audit_logs')

    @validates('user_ip')
    def validate_ip(self, key, value):
        try:
            ipaddress.ip_address(value)
        except ValueError:
            raise ValueError(f'Error with {key!r}: Provided value is not a valid IP address')
        return value

    __table_args__ = (
        Index('idx_audit_user_id', user_id),
        Index('idx_audit_user_ip', user_ip),
        Index('idx_audit_created_at', 'created_at'),
        Index('idx_audit_updated_at', 'updated_at')
    )

    def __repr__(self):
        return (
                f"<AuditLog(id={self.id}, user_id={self.user_id}, "
                f"user_ip='{self.user_ip}', action='{self.action}', "
                f"details='{self.details}', status={self.status}, "
                f"created_at={self.created_at}, updated_at={self.updated_at}"
                ")>"
               )

# ==== Helper Models ====

# clearance lvls for users and
# classification lvls for scps
class ClearanceLvl(HelperTableMixin, Base):
    __tablename__ = 'clearance_lvls'

    # relationships
    users: Mapped[list["User"]] = rel('User', back_pop='clearance_lvl')
    scps: Mapped[list["SCP"]] = rel('SCP', back_pop='clearance_lvl')

    __table_args__ = (
        Index(f'idx_clearance_lvls_name', 'name'),
        Index(f'idx_clearance_lvls_updated_at', 'updated_at')
    )

    def __repr__(self):
        return (
                f"<ClearanceLvl(id={self.id}, name='{self.name}', "
                f"created_at={self.created_at}, updated_at={self.updated_at}"
                ")>"
               )


# SCP specific models
class ContainmentClass(HelperTableMixin, Base):
    __tablename__ = 'containment_classes'

    # relationships
    scps: Mapped[list["SCP"]] = rel('SCP', back_pop='containment_class')

    __table_args__ = (
        Index(f'idx_containment_classes_name', 'name'),
        Index(f'idx_containment_classes_updated_at', 'updated_at')
    )

    def __repr__(self):
        return (
                f"<ContainmentClass(id={self.id}, name='{self.name}', "
                f"created_at={self.created_at}, updated_at={self.updated_at}"
                ")>"
               )

class SecondaryClass(HelperTableMixin, Base):
    __tablename__ = 'secondary_classes'

    # relationships
    scps: Mapped[list["SCP"]] = rel('SCP', back_pop='secondary_class')

    __table_args__ = (
        Index(f'idx_secondary_classes_name', 'name'),
        Index(f'idx_secondary_classes_updated_at', 'updated_at')
    )

    def __repr__(self):
        return (
                f"<SecondaryClass(id={self.id}, name='{self.name}', "
                f"created_at={self.created_at}, updated_at={self.updated_at}"
                ")>"
               )

class DisruptionClass(HelperTableMixin, Base):
    __tablename__ = 'disruption_classes'

    # relationships
    scps: Mapped[list["SCP"]] = rel('SCP', back_pop='disruption_class')

    __table_args__ = (
        Index(f'idx_disruption_classes_name', 'name'),
        Index(f'idx_disruption_classes_updated_at', 'updated_at')
    )

    def __repr__(self):
        return (
                f"<DisruptionClass(id={self.id}, name='{self.name}', "
                f"created_at={self.created_at}, updated_at={self.updated_at}"
                ")>"
               )

class RiskClass(HelperTableMixin, Base):
    __tablename__ = 'risk_classes'

    # relationships
    scps: Mapped[list["SCP"]] = rel('SCP', back_pop='risk_class')

    __table_args__ = (
        Index(f'idx_risk_classes_name', 'name'),
        Index(f'idx_risk_classes_updated_at', 'updated_at')
    )

    def __repr__(self):
        return (
                f"<RiskClass(id={self.id}, name='{self.name}', "
                f"created_at={self.created_at}, updated_at={self.updated_at}"
                ")>"
               )


# all user titles
class Title(HelperTableMixin, Base):
    __tablename__ = 'titles'

    # relationships
    users: Mapped[list["User"]] = rel('User', back_pop='title')

    __table_args__ = (
        Index(f'idx_titles_name', 'name'),
        Index(f'idx_titles_updated_at', 'updated_at')
    )

    def __repr__(self):
        return (
                f"<Title(id={self.id}, name='{self.name}', "
                f"created_at={self.created_at}, updated_at={self.updated_at}"
                ")>"
               )


# ==== Table related lists & funcs ====

VALID_TABLES = [
    'users',
    'scps',
    'mtfs',
    'sites',
    'audit_log',

    'clearance_lvls',
    'containment_classes',
    'secondary_classes',
    'disruption_classes',
    'risk_classes',
    'titles',
]
"""Valid table names for SQL queries"""

VALID_MODELS = [
    # main tables
    'User',
    'SCP',
    'MTF',
    'Site',
    'AuditLog',

    # helper tables
    'ClearanceLvl',
    'ContainmentClass',
    'SecondaryClass',
    'DisruptionClass',
    'RiskClass',
    'Title',
]
"""Valid model names for SQLAlchemy"""


# checks `table` against valid_tables
def validate_table(table: str) -> bool:
    """
    Validate the table name against the list of valid tables.

    Returns True if the table is valid, False otherwise.
    """
    return table in VALID_TABLES


# ==== namespaces ====
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
