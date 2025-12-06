"""
Helpers to process null values for bar templates
"""

from ..display.config import CLEAR_LVL_COLOURS
from .models import Models

from dataclasses import dataclass


# dataclasses for processed data


class ProcessedData:

    @dataclass
    class SCP:
        id: int
        name: str
        clear_lvl_str: str
        clear_lvl_id: int

        cnt_class: str
        scnd_class: str

        disrupt_class: str
        disrupt_class_hex: str | None

        risk_class: str
        risk_class_hex: str | None

        site_resp: str
        mtf_str: str


    @dataclass
    class Site:
        name_str: str
        director_str: str


    @dataclass
    class MTF:
        name_str: str
        site: str
        leader_str: str
        active: str


    @dataclass
    class User:
        name_str: str
        site: str
        clearance: str


def scp(info: Models.SCP) -> ProcessedData.SCP:

    # === Process null values ===
    if info.secondary_class:
        scnd_class = info.secondary_class.name
    else:
        scnd_class = 'None'

    if info.disruption_class:
        disrupt_class = info.disruption_class.name
        disrupt_class_hex = CLEAR_LVL_COLOURS[info.disruption_class.id]
    else:
        disrupt_class = '[DATA EXPUNGED]'
        disrupt_class_hex = None

    if info.risk_class:
        risk_class = info.risk_class.name
        risk_class_hex = CLEAR_LVL_COLOURS[info.risk_class.id]
    else:
        risk_class = '[DATA EXPUNGED]'
        risk_class_hex = None

    if info.site_responsible_id:
        site_resp = f'Site-{info.site_responsible_id:03d}'
    else:
        site_resp = '[DATA EXPUNGED]'

    if info.mtf:
        mtf_str = (f'{info.mtf.name} "{info.mtf.nickname}"'
                   f' (ID: {info.mtf.id:03d})')
    else:
        mtf_str = 'None'

    # === Return processed data ===
    return ProcessedData.SCP(
        id = info.id,
        name = info.name,

        clear_lvl_str = info.clearance_lvl.name,
        clear_lvl_id = info.clearance_lvl.id,

        cnt_class = info.containment_class.name,
        scnd_class = scnd_class,

        disrupt_class = disrupt_class,
        disrupt_class_hex = disrupt_class_hex,
        risk_class = risk_class,
        risk_class_hex = risk_class_hex,

        site_resp = site_resp,
        mtf_str = mtf_str,
    )


def site(info: Models.Site) -> ProcessedData.Site:

    if info.director:
        director_str = (f'{info.director.name} '
                        f'(ID: {info.director.id})')

    else:
        director_str = '[DATA EXPUNGED]'

    return ProcessedData.Site(
        name_str = f'{info.name} (ID: {info.id:03d})',
        director_str = director_str,
    )


def mtf(info: Models.MTF) -> ProcessedData.MTF:
    if info.site:
        site_name = f'Site-{info.site.id:03d}'
    else:
        site_name = '[DATA EXPUNGED]'

    if info.leader:
        leader_str = (f'{info.leader.name} '
                      f'(ID: {info.leader.id})')
    else:
        leader_str = '[DATA EXPUNGED]'

    active = 'Yes' if info.active else 'No'

    name_str = f'MTF {info.name} "{info.nickname}" (MTF ID: {info.id})'

    return ProcessedData.MTF(
        name_str = name_str,
        site = site_name,
        leader_str = leader_str,
        active = active
    )


def user(info: Models.User) -> ProcessedData.User:
    name_str = f'{info.title.name} {info.name} (ID: {info.id})'

    return ProcessedData.User(
        name_str = name_str,
        site = f'Site-{info.site_id:03d}',
        clearance = info.clearance_lvl.name
    )
