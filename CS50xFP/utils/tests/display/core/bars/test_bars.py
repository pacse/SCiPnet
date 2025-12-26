import pytest

from .....display.core.bars.bars import (acs_bar, mtf_bar, site_bar, user_bar)
from .....sql import null_processors as nps
from .....sql.null_processors import Models as PD

from ....testdata import TestData

@pytest.mark.bars
def test_acs_bar(scp_info: Models.SCP):
    """Tests acs_bar function"""
    acs_bar(scp_info)

@pytest.mark.bars
def test_mtf_bar(mtf_info: Models.MTF):
    """Tests mtf_bar function"""
    mtf_bar(mtf_info)

@pytest.mark.bars
def test_site_bar(site_info: Models.Site):
    """Tests site_bar function"""
    site_bar(site_info, loc="Test Location")

@pytest.mark.bars
def test_user_bar(user_info: Models.User):
    """Tests user_bar function"""
    user_bar(user_info)


def test_all_scps():
    for scp in TestData.SCPS:
        scp_info = nps.scp(scp)
        acs_bar(scp_info)

def test_all_mtfs():
    for mtf in TestData.MTFS:
        mtf_info = nps.mtf(mtf)
        mtf_bar(mtf_info)

def test_all_sites():
    for site in TestData.SITES:
        site_info = nps.site(site)
        site_bar(site_info, loc="Test Location")

def test_all_users():
    for user in TestData.USERS:
        user_info = nps.user(user)
        user_bar(user_info)
