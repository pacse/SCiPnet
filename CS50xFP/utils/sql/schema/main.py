"""
Main DB table definitions
"""

from .base import ORMBase, MainTableMixin, col_int_fk, col_str, wk_hash, \
                  col_datetime, rel, WK_HASH_REGEX
from .helpers import ClearanceLvl, ContainmentClass, SecondaryClass, \
                     Title, DisruptionClass, RiskClass

from sqlalchemy import Column, Boolean
from sqlalchemy.orm import validates, Mapped

import re
import ipaddress



class User(MainTableMixin, ORMBase):
    __tablename__ = 'users'


    name = col_str(50, nullable = False)
    password = wk_hash(nullable = False)
    override_phrase = wk_hash(nullable = True)

    clearance_lvl_id = col_int_fk('clearance_lvls.id', nullable = False)

    title_id = col_int_fk('titles.id', nullable = False)
    site_id = col_int_fk('sites.id', nullable = False)
    mtf_id = col_int_fk('mtfs.id', nullable = True)

    is_active = Column(Boolean, default = False, nullable = False)
    last_login = col_datetime(nullable = True)

    # relationships

    # local
    clearance_lvl: Mapped["ClearanceLvl"] = rel('users')
    title: Mapped["Title"] = rel('users')
    site: Mapped["Site"] = rel('staff', keys=[site_id])
    mtf: Mapped["MTF | None"] = rel('leader', keys=[mtf_id])

    # acknowledge other tables
    audit_logs: Mapped[list["AuditLog"]] = rel('user')
    led_mtfs: Mapped[list["MTF"]] = rel('members', keys='MTF.leader_id')
    directed_sites: Mapped[list["Site"]] = rel(
                                               'director',
                                               keys='Site.director_id'
                                              )

    # validator! 🎉
    @validates('password', 'override_phrase')
    def validate_hash(self, key: str, value: str) -> str:
        """
        Validates Werkzeug password hash format

        Parameters
        ----------
        key : str
            The name of the attribute being validated
        value : str
            The value being assigned to the attribute

        Raises
        ------
        ValueError
            - If `value` does not match Werkzeug hash format

        Returns
        -------
        str
            The validated value
        """
        if not re.fullmatch(WK_HASH_REGEX, value):
            raise ValueError(
                             f'Error with {key!r}: '
                             'Provided value is not a valid Werkzeug hash'
                            )
        return value


class SCP(MainTableMixin, ORMBase):
    __tablename__ = 'scps'

    name = col_str(100, nullable=False) # eg. 'The "Living" Room' (002)

    clearance_lvl_id = col_int_fk('clearance_lvls.id', False)

    containment_class_id = col_int_fk('containment_classes.id', False)
    secondary_class_id = col_int_fk('secondary_classes.id', True)

    disruption_class_id = col_int_fk('disruption_classes.id', True)
    risk_class_id = col_int_fk('risk_classes.id', True)

    site_responsible_id = col_int_fk('sites.id', True)
    assigned_task_force_id = col_int_fk('mtfs.id', True)

    # relationships

    # local
    clearance_lvl: Mapped["ClearanceLvl"] = rel('scps')

    containment_class: Mapped["ContainmentClass"] = rel('scps')
    secondary_class: Mapped["SecondaryClass | None"] = rel('scps')
    disruption_class: Mapped["DisruptionClass | None"] = rel('scps')
    risk_class: Mapped["RiskClass | None"] = rel('scps')

    site_responsible: Mapped["Site | None"] = rel('scps')
    mtf: Mapped["MTF | None"] = rel('scps')


class MTF(MainTableMixin, ORMBase):
    __tablename__ = 'mtfs'

    name = col_str(25, nullable=False) # eg. Epsilon-6
    nickname = col_str(100, nullable=False) # eg. 'Village Idiots', long just in case

    leader_id = col_int_fk('users.id', nullable=True)
    site_id = col_int_fk('sites.id', nullable=True)

    active = Column(Boolean, default=True, nullable=False)

    # relationships

    # local
    leader: Mapped["User | None"] = rel('led_mtfs', keys=[leader_id])
    site: Mapped["Site | None"] = rel('mtfs')

    # acknowledge other tables
    scps: Mapped[list["SCP"]] = rel('mtf')
    members: Mapped[list["User"]] = rel('mtf', keys='User.mtf_id')


class Site(MainTableMixin, ORMBase):
    __tablename__ = 'sites'

    name = col_str(100, False) # eg. 'Site-01'
    director_id = col_int_fk('users.id', True)

    # relationships

    # local
    director: Mapped["User | None"] = rel(
                                          'directed_sites',
                                          keys=[director_id]
                                         )

    # acknowledge other tables
    scps: Mapped[list["SCP"]] = rel('site_responsible')
    mtfs: Mapped[list["MTF"]] = rel('site')
    staff: Mapped[list["User"]] = rel('site', keys='User.site_id')


class AuditLog(MainTableMixin, ORMBase):
    __tablename__ = 'audit_log'

    user_id = col_int_fk('users.id', nullable=False)
    user_ip = col_str(60, nullable=False) # IP address of the user, long enough for IPv6, i think

    action = col_str(255, nullable=False) # description of action taken
    details = col_str(255, nullable=False) # additional details about the action
    status = Column(Boolean, nullable=False) # success or failure of the action


    # acknowledge user relationship
    user: Mapped["User"] = rel('audit_logs')

    @validates('user_ip')
    def validate_ip(self, key: str, value: str) -> str:
        try:
            ipaddress.ip_address(value)
        except ValueError as e:
            raise ValueError(
                             f'Error with {key!r}: '
                             f'Invalid IP address {value!r}: {e}'
                            ) from e
        return value
