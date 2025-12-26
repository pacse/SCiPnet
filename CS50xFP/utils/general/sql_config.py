"""
Database configuration settings
Controls db conn params and pooling settings

Contains
--------
- Paths
    - PROJECT_ROOT
    - DEEPWELL_DIR
    - DB_PATH
    - DB_URL

- SQLAlchemy Config
    - POOL_CONFIG
    - SQLITE_CONFIG

- Other Config
    - EXPUNGED
    - NONE_STR

Notes
-----
- Made primarily by Github Copilot
"""

from pathlib import Path



# === Paths ===
PROJECT_ROOT = Path(__file__).parents[2].resolve()
"""Path to project root (`CS50xFP/`)"""
DEEPWELL_DIR = PROJECT_ROOT / 'deepwell'
"""Path to the `deepwell/` directory"""
DB_PATH = DEEPWELL_DIR / 'SCiPnet.db'
"""Path to the SQLite database"""

DB_URL = f'sqlite:///{DB_PATH}'
"""URL to connect to the database"""



# === SQLAlchemy Config ===
_DEBUG_MODE = True
"""Whether to run the database in debug mode (echo SQL queries)"""

POOL_CONFIG = {
    'pool_size': 5,        # num of permanent db conns
    'max_overflow': 10,    # max num of additional db conns
    'pool_timeout': 30,    # seconds to wait for an available conn before throwing an error
    'pool_recycle': 3600,  # seconds to recycle conns
    'pool_pre_ping': True  # test connections before using them
}
"""Connection pool configuration"""

SQLITE_CONFIG = {
    'isolation_level': 'READ COMMITTED',  # only see commited data, allows for higher throughput than SERIALIZABLE while still being safe
    'echo': _DEBUG_MODE,                   # log SQL queries in debug mode
    'connect_args': {
        'timeout': 30,                    # seconds to wait for transaction completion
        'check_same_thread': False        # allow conns to be shared across threads (allow multithreading)
    }
}
"""SQLite specific configuration"""



# === Other Config ===

EXPUNGED = '[DATA EXPUNGED]'
NONE_STR = 'None'



# === Exports ===

# namespaces

class Config:
    POOL = POOL_CONFIG
    SQLITE = SQLITE_CONFIG

class Paths:
    PROJECT_ROOT = PROJECT_ROOT
    DEEPWELL_DIR = DEEPWELL_DIR
    DB_PATH = DB_PATH
    DB_URL = DB_URL


__all__ = [
           # Paths
           'PROJECT_ROOT',
           'DEEPWELL_DIR',
           'DB_PATH',
           'DB_URL',

           # SQLAlchemy Config
           '_DEBUG_MODE',
           'POOL_CONFIG',
           'SQLITE_CONFIG',

           # Namespaces
           'Config',
           'Paths',
          ]
