# projects.py
# (C) 2021 Marquis Kurt, Nodar Sotkilava, and Unscripted VN Team.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from .utils import DatabaseContext
from psycopg2.extras import RealDictCursor
from psycopg2.sql import SQL

def get_projects(in_app_db) -> dict:
    """Returns a list of all projects."""
    with DatabaseContext(in_app_db, cursor_factory=RealDictCursor) as cur:
        cur.execute('select * from Project')
        return cur.fetchall()

def get_project(in_app_db, project_id: str) -> dict:
    """Returns the row in the projects table with a specified ID."""
    with DatabaseContext(in_app_db, cursor_factory=RealDictCursor) as cur:
        cur.execute(SQL("select * from Project where projectId = {}").format(project_id))
        return cur.fetchone()