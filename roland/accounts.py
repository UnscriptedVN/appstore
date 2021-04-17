# projects.py
# (C) 2021 Marquis Kurt, Nodar Sotkilava, and Unscripted VN Team.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from .utils import DatabaseContext
from psycopg2.extras import RealDictCursor, RealDictRow
from psycopg2.sql import SQL
from enum import IntEnum

class AccountType(IntEnum):
    """An enum that represents the diffrent account types."""
    UserAccount = 0
    Developer = 1
    Curator = 2


def __get_account_type(account: RealDictRow) -> RealDictRow:
    pass


def get_account(in_app_db, userId: str) -> dict:
    """Returns the row in the accounts projects table with a specified ID."""
    with DatabaseContext(in_app_db, cursor_factory =RealDictCursor) as cur:
        comm = SQL("select * from Account where userId = %s")
        cur.execute(comm, [userId])
        return cur.fetchall()




