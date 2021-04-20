# lists.py
# (C) 2021 Marquis Kurt, Nodar Sotkilava, and Unscripted VN Team.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https: //mozilla.org/MPL/2.0/.

# TODO: Add infastracture for Curator lists
from .utils import DatabaseContext
from psycopg2.extras import RealDictCursor, RealDictRow
from psycopg2.sql import SQL

def get_all_curator_lists(in_app_db) -> dict:
    """Return all curated lists"""
    with DatabaseContext(in_app_db, cursor_factory = RealDictCursor) as cur:
        comm = SQL("select * from List")
        cur.execute(comm)
        return cur.fetchall()

def get_one_list(in_app_db, listId: str) -> dict:
    """Returns a curated list for a given list Id"""
    with DatabaseContext(in_app_db, cursor_factory=RealDictCursor) as cur:
        comm = SQL("select * from List where listId = %s")
        cur.execute(comm, [listId])
        return cur.fetchall()
        
def get_curator_lists(in_app_db, userId: str) -> dict:
    """Returns all the lists that a Curator made"""
    with DatabaseContext(in_app_db, cursor_factory=RealDictCursor) as cur:
        comm = SQL("select * from List where userId = %s")
        cur.execute(comm, [userId])
        return cur.fetchall()

def get_project_in_curator_list(in_app_db, project_id: str) -> dict:
    """Returns all the lists that a project is in"""
    with DatabaseContext(in_app_db, cursor_factory=RealDictCursor) as cur:
        comm = SQL("select * from Includes where projectId = %s")
        cur.execute(comm, [project_id])
        return cur.fetchall()