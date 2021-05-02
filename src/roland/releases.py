# releases.py
# (C) 2021 Marquis Kurt, Nodar Sotkilava, and Unscripted VN Team.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https: //mozilla.org/MPL/2.0/.

from enum import IntEnum
from psycopg2.sql import SQL
from psycopg2.extras import RealDictCursor, RealDictRow
from .utils import DatabaseContext

class ReleaseStatus(IntEnum):
    """An enumeration representing the different release status codes."""
    PendingReview = 0
    Approved = 1
    Rejected = 2


def get_pending_releases(in_app_db) -> dict:
    with DatabaseContext(in_app_db, cursor_factory=RealDictCursor) as cursor:
        command = SQL("select * from Release where inspectStatus = %s")
        cursor.execute(command, [ReleaseStatus.PendingReview.value])
        return cursor.fetchall()

def transform_release_row(release_row: RealDictRow) -> RealDictRow:
    api_mode = release_row.copy()
    api_mode["download"] = api_mode["downloadurl"]
    api_mode["release_date"] = api_mode["inspectdate"]
    del api_mode["downloadurl"], api_mode["inspectstatus"], api_mode["userid"], api_mode["projectid"], \
        api_mode["inspectdate"]
    return api_mode


def create_release(in_app_db, project_id: str, version: str, download: str, notes: str, developer_id):
    with DatabaseContext(in_app_db) as cursor:
        command = SQL(
            "insert into Release (version, notes, downloadUrl, projectId, inspectStatus, userId) values (%s, %s, %s, %s, %s, %s)")
        cursor.execute(command, [version, notes, download, project_id, ReleaseStatus.PendingReview.value, developer_id])
        in_app_db.commit()


def assign_release(in_app_db, project_id: str, version: str, to_curator: int):
    """Assign a curator to a specified release pending review."""
    with DatabaseContext(in_app_db) as cursor:
        command = SQL("update Release set userId = %s where version = %s and projectId = %s and inspectStatus = %s")
        cursor.execute(command, [to_curator, version, project_id, ReleaseStatus.PendingReview.value])
        in_app_db.commit()
        
def get_release(in_app_db, project_id: str) -> dict:
    """Get the release waiting review"""
    with DatabaseContext(in_app_db, cursor_factory=RealDictCursor) as cursor:
        command = SQL("select * from Release where projectId = %s and inspectStatus = %s")
        cursor.execute(command, [project_id, ReleaseStatus.PendingReview.value])
        return cursor.fetchall()
        
def approve_release(in_app_db, project_id: str):
    """Approve release"""
    with DatabaseContext(in_app_db) as cursor:
        command = SQL("update Release set inspectStatus = 1, inspectDate = now() where projectId = %s")
        cursor.execute(command, [project_id])
        in_app_db.commit()

def reject_release(in_app_db, project_id: str):
    """Reject release"""
    with DatabaseContext(in_app_db) as cursor:
        command = SQL("update Release set inspectStatus = 2, inspectDate = now() where projectId = %s")
        cursor.execute(command, [project_id])
        in_app_db.commit()