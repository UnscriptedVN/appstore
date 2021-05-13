# releases.py
# (C) 2021 Marquis Kurt, Nodar Sotkilava, and Unscripted VN Team.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https: //mozilla.org/MPL/2.0/.

from enum import IntEnum
from psycopg2.sql import SQL
from psycopg2.extras import RealDictCursor, RealDictRow
from random import shuffle
from .utils import DatabaseContext

class ReleaseStatus(IntEnum):
    """An enumeration representing the different release status codes."""
    PendingReview = 0
    Approved = 1
    Rejected = 2

def __get_random_curator(in_app_db, excluding_id=None) -> int:
    """Returns a random user ID that corresponds to a curator."""
    with DatabaseContext(in_app_db, cursor_factory=RealDictCursor) as cursor:
        command = SQL("select userId from Account where accountType = %s")
        cursor.execute(command, [2])
        ids = [int(row["userid"]) for row in cursor.fetchall() if int(row["userid"]) != excluding_id]
        shuffle(ids)
        return ids[0] if len(ids) > 0 else -1



def get_pending_releases(in_app_db) -> dict:
    """Returns a dictionary of all Releases awaiting review."""
    with DatabaseContext(in_app_db, cursor_factory=RealDictCursor) as cursor:
        command = SQL("select * from Release where inspectStatus = %s")
        cursor.execute(command, [ReleaseStatus.PendingReview.value])
        return cursor.fetchall()

def transform_release_row(release_row: RealDictRow) -> RealDictRow:
    """Transforms the metadata of a release so that it's easier to read."""
    api_mode = release_row.copy()
    api_mode["download"] = api_mode["downloadurl"]
    api_mode["release_date"] = api_mode["inspectdate"]
    del api_mode["downloadurl"], api_mode["inspectstatus"], api_mode["userid"], api_mode["projectid"], \
        api_mode["inspectdate"]
    return api_mode


def create_release(in_app_db, project_id: str, version: str, download: str, notes: str, developer_id):
    """Creates a new Release"""
    assigned_curator = __get_random_curator(in_app_db, excluding_id=developer_id)
    with DatabaseContext(in_app_db) as cursor:
        command = SQL(
            "insert into Release (version, notes, downloadUrl, projectId, inspectStatus, userId) values (%s, %s, %s, %s, %s, %s)")
        cursor.execute(command, [version, notes, download, project_id, ReleaseStatus.PendingReview.value, assigned_curator])
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
        
def approve_release(in_app_db, project_id: str, version: str):
    """Approve release"""
    with DatabaseContext(in_app_db) as cursor:
        command = SQL("update Release set inspectStatus = 1, inspectDate = now() where projectId = %s and version = %s")
        cursor.execute(command, [project_id, version])
        in_app_db.commit()

def reject_release(in_app_db, project_id: str, version: str, curator: int, message:str = "Contact the team."):
    """Reject release"""
    with DatabaseContext(in_app_db) as cursor:
        reject_command = SQL("update Release set inspectStatus = 2, inspectDate = now() where projectId = %s")
        cursor.execute(reject_command, [project_id])
        
        author_message = SQL("Insert into Message values (now(), %s, %s, %s, %s)")
        cursor.execute(author_message, [curator, project_id, version, message])
        
        in_app_db.commit()
        
def get_messages(in_app_db, project_id: str):
	"""Returns the action center messages associated with a given project."""
	with DatabaseContext(in_app_db, cursor_factory=RealDictCursor) as cursor:
		command = SQL("select * from Message where projectId = %s order by writeDate desc")
		cursor.execute(command, [project_id])
		return cursor.fetchall()
