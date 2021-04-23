# editor.py
# (C) 2021 Marquis Kurt, Nodar Sotkilava, and Unscripted VN Team.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https: //mozilla.org/MPL/2.0/.

from psycopg2.sql import SQL
from psycopg2.extras import RealDictCursor, RealDictRow
from .projects import ProjectType
from .utils import DatabaseContext

def create_project(
    in_app_db, from_developer_id: int, name: str, identifier: str, type: ProjectType, tagline: str, license: int = 1):
    with DatabaseContext(in_app_db) as cursor:
        new_app_command = SQL("insert into Project values (%s, %s, %s, '0.0.0', %s, null, %s, null)")
        cursor.execute(new_app_command, [identifier, type.value, name, tagline, license])

        link_to_developer_command = SQL("insert into Maintains values (%s, %s)")
        cursor.execute(link_to_developer_command, [identifier, from_developer_id])
        in_app_db.commit()

def update_project_licensing(in_app_db, project_id: str, license: int = 1):
    with DatabaseContext(in_app_db) as cursor:
        command = SQL("update Project set licenseId = %s where projectId = %s")
        cursor.execute(command, [license, project_id])
        in_app_db.commit()