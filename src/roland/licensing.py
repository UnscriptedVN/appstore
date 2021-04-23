# licensing.py
# (C) 2021 Marquis Kurt, Nodar Sotkilava, and Unscripted VN Team.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https: //mozilla.org/MPL/2.0/.

from typing import Optional
from psycopg2.sql import SQL
from psycopg2.extras import RealDictCursor, RealDictRow
from .utils import DatabaseContext


def get_project_license(in_app_db, license_id) -> Optional[str]:
    with DatabaseContext(in_app_db, cursor_factory=RealDictCursor) as cursor:
        command = SQL("select licenseName from License where licenseId = %s")
        cursor.execute(command, [license_id])
        result = cursor.fetchone()

    if not result:
        return None
    return result["licensename"]

def get_all_licenses(in_app_db) -> dict:
    with DatabaseContext(in_app_db, cursor_factory=RealDictCursor) as cursor:
        command = SQL("select * from License")
        cursor.execute(command)
        return cursor.fetchall()