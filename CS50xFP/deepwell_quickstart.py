"""
Script to recreate the sql database
usage: python quickstart.py [DB Name (optional)]
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sys import argv
import os

# models to create tables
from utils.sql.schema import ORMBase, MainModels, HelperModels

from werkzeug.security import generate_password_hash

# handle cl args
if len(argv) > 2:
    # improper usage
    raise ValueError(f'Improper usage:\nExpected `python {argv[0]} [DB Name (optional)]`')

elif len(argv) == 2:
    # we have a db name
    name = argv[1]

else:
    # use default
    name = 'SCiPNET.db'

# remove old db if exists
if os.path.exists(f'deepwell/{name}'):
    os.remove(f'deepwell/{name}')
    print(f'Removed old database (deepwell/{name})')

# create engine & session
engine = create_engine(f'sqlite:///deepwell/{name}')
session = sessionmaker(bind=engine)()

print(f'Creating new database (deepwell/{name}) . . .')

# ==== create all tables ====
ORMBase.metadata.create_all(engine)


print(f'Adding initial data . . .')

# ==== add initial data ====

# helper tables

for c_lvl in [
              'Level 1 - Unrestricted',
              'Level 2 - Restricted',
              'Level 3 - Confidential',
              'Level 4 - Secret',
              'Level 5 - Top Secret',
              'Level 6 - Cosmic Top Secret'
             ]:
    session.add(
        HelperModels.ClearanceLvl(name=c_lvl)
        )

for c_clss in [
               'Safe',
               'Euclid',
               'Keter',
               'Neutralized',
               'Explained',
               'Decommissioned',
               'Uncontained',
               'Pending'
              ]:
    session.add(
        HelperModels.ContainmentClass(name=c_clss)
        )


for d_clss in [
               'Level 1 - Dark',
               'Level 2 - Vlam',
               'Level 3 - Keneq',
               'Level 4 - Ekhi',
               'Level 5 - Amida'
              ]:
    session.add(
        HelperModels.DisruptionClass(name=d_clss)
        )

for r_clss in [
               'Level 1 - Notice',
               'Level 2 - Caution',
               'Level 3 - Warning',
               'Level 4 - Danger',
               'Level 5 - Critical'
              ]:
    session.add(
        HelperModels.RiskClass(name=r_clss)
        )

for title in [
              'Containment Specialist',
              'Researcher',
              'Security Officer',
              'Tactical Response Officer',
              'Field Agent',
              'Mobile Task Force Operative',
              'Site Director',
              'O5 Council Member'
             ]:
    session.add(
        HelperModels.Title(name=title)
        )


# old data
print(f'Initializing old data . . .')

s_1123 = MainModels.Site(id=1123, name='MEEEEE')
s_6 = MainModels.Site(id=6, name='Site-6')


u_1 = MainModels.User(name='Evren Packard', password=generate_password_hash('InSAne'),
                      clearance_lvl_id=6, title_id=7, site_id=1123,
                      override_phrase=generate_password_hash('You\'ll be living a life like Barbie and Ken'))
u_2 = MainModels.User(name='Glorbo Florbo', password=generate_password_hash('1234'),
                      clearance_lvl_id=5, title_id=6, site_id=1123)
u_3 = MainModels.User(name='James', password=generate_password_hash('password'),
                      clearance_lvl_id=1, title_id=6, site_id=6)

mtf_1 = MainModels.MTF(name='Gamma-94', nickname='Gramma\'s little helpers',
                       leader_id=3, site_id=1123)
mtf_2 = MainModels.MTF(name='Epsilon-6', nickname='Village Idiots',)
mtf_3 = MainModels.MTF(name='Alpha-1', nickname='Red Right Hand')

scp_1 = MainModels.SCP(id=49, name='Plague Doctor', clearance_lvl_id=6,
                       containment_class_id=2, disruption_class_id=2,
                       risk_class_id=4, site_responsible_id=1123, assigned_task_force_id=1)
scp_2 = MainModels.SCP(id=2, name="The 'Living' Room", clearance_lvl_id=2,
                       containment_class_id=2, disruption_class_id=1,
                       risk_class_id=2)

print(f'Adding old data . . .')

session.add_all([s_1123, s_6,
                 u_1, u_2, u_3,
                 mtf_1, mtf_2, mtf_3,
                 scp_1, scp_2
                ])

session.commit()
print('\nSuccess!!!')
