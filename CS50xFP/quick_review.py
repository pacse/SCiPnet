"""
Quick bar review script - run from project root
"""

from utils.display.core.bars.bars import (acs_bar, mtf_bar, site_bar, user_bar)
from utils.tests.testdata import TestData
from rich.console import Console
from os import system as sys, name as os_name

console = Console()

# Review all SCPs
def scp_review():
    print("\n" + "="*80)
    print("SCP BARS")
    print("="*80)
    for scp in TestData.SCPS:
        print()
        acs_bar(scp, console)
        print()

# Review all MTFs
def mtf_review():
    print("\n" + "="*80)
    print("MTF BARS")
    print("="*80)
    for mtf in TestData.MTFS:
        print()
        mtf_bar(mtf, console)
        print()

# Review all Sites
def site_review():
    print("\n" + "="*80)
    print("SITE BARS")
    print("="*80)
    for site in TestData.SITES:
        print()
        site_bar(site, "Test Location", console)
        print()

# Review all Users
def user_review():
    print("\n" + "="*80)
    print("USER BARS")
    print("="*80)
    for user in TestData.USERS:
        print()
        user_bar(user, console)
        print()

if __name__ == "__main__":
    for i, func in enumerate([
        scp_review,
        mtf_review,
        site_review,
        user_review
    ], start=1):
        sys('cls' if os_name == 'nt' else 'clear')
        func()
        input(f"Press Enter to continue... (Page {i}/4)")

sys('cls' if os_name == 'nt' else 'clear')
