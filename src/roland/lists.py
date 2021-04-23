# lists.py
# (C) 2021 Marquis Kurt, Nodar Sotkilava, and Unscripted VN Team.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https: //mozilla.org/MPL/2.0/.

# TODO: Add infastracture for Curator lists
from .utils import DatabaseContext
from psycopg2.extras import RealDictCursor, RealDictRow
from psycopg2.sql import SQL
from .projects import _transform_project_data

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
        return cur.fetchone()
        
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

def get_projects_from_list(in_app_db, list_id: str) -> list:
    with DatabaseContext(in_app_db, cursor_factory=RealDictCursor) as cursor:
        command = SQL("select * from (Project join Includes using (projectId)) where listId = %s")
        cursor.execute(command, [list_id])
        return [_transform_project_data(s, in_app_db) for s in cursor.fetchall()]

def create_list(in_app_db, list_name: str, list_blurb: str, list_apps, with_curator: str):
    projects = list_apps if list_apps else []
    with DatabaseContext(in_app_db, cursor_factory=RealDictCursor) as cursor:
        spawner = SQL("insert into List (name, blurb, userId) values (%s, %s, %s)")
        cursor.execute(spawner, [list_name, list_blurb, with_curator])

        new_id_finder = SQL("select listId from List where name = %s and userId = %s")
        cursor.execute(new_id_finder, [list_name, with_curator])

        new_id = cursor.fetchone()
        if new_id:
            for project in projects:
                command = SQL("insert into Includes values (%s, %s)")
                cursor.execute(command, [new_id["listid"], project])
        
        in_app_db.commit()
        return new_id.listid

def update_list(in_app_db, list_id, new_name, new_blurb):
    with DatabaseContext(in_app_db) as cursor:
        command = SQL("update List set name = %s, blurb = %s where listId = %s")
        cursor.execute(command, [new_name, new_blurb, list_id])
        in_app_db.commit()


def delete_list(in_app_db, list_id):
    projects_in_list = get_projects_from_list(in_app_db, list_id)
    with DatabaseContext(in_app_db, cursor_factory=RealDictCursor) as cursor:
        for project in projects_in_list:
            deletor = SQL("delete from Includes where projectId = %s and listId = %s")
            cursor.execute(deletor, [project["id"], list_id])
        
        deletor_list = SQL("delete from List where listId = %s")
        cursor.execute(deletor_list, [list_id])
        in_app_db.commit()