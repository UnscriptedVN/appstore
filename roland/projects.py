# projects.py
# (C) 2021 Marquis Kurt, Nodar Sotkilava, and Unscripted VN Team.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from typing import Optional
from .utils import DatabaseContext
from psycopg2.extras import RealDictCursor, RealDictRow
from psycopg2.sql import SQL
from enum import IntEnum

class ProjectType(IntEnum):
    """An enum that represents the different project types."""
    App = 0
    CoreService = 1
    Framework = 2


def __transform_project_data(project: RealDictRow, appdb=None) -> RealDictRow:
    """Returns a transformed version of the project data, or itself if the project doesn't exist."""
    if not project:
        return project
    new_project = project.copy()
    
    # Re-map project fields for API.
    new_project["id"] = new_project["projectid"]
    new_project["latest_version"] = new_project["version"]
    new_project["license"] = get_project_license(appdb, new_project["licenseid"])
    new_project["icon"] = new_project["projecticon"]
    del new_project["projectid"]
    del new_project["version"]
    del new_project["projecticon"]
    del new_project["licenseid"]

    # Add new fields based on context.
    new_project["developer"] = get_developer(appdb, new_project["id"])["userid"]
    new_project["releases"] = get_releases(appdb, new_project["id"])
    new_project["screenshots"] = get_screenshots(appdb, new_project["id"])
    new_project["permissions"] = get_project_permissions(
        appdb, new_project["id"])
    
    new_project["type"] = str(ProjectType(new_project["type"]).name).lower()
    return new_project

def list_projects(in_app_db) -> list:
    """Returns a list of all projects."""
    with DatabaseContext(in_app_db, cursor_factory=RealDictCursor) as cur:
        cur.execute('select * from Project')
        data = cur.fetchall().copy()
    projects = []
    for project in data:
        projects.append(__transform_project_data(project, in_app_db))
    return projects

def get_project(in_app_db, project_id: str) -> dict:
    """Returns the row in the projects table with a specified ID."""
    with DatabaseContext(in_app_db, cursor_factory=RealDictCursor) as cur:
        comm = SQL("select * from Project where projectid = %s")
        cur.execute(comm, [project_id])
        real_project_data = __transform_project_data(cur.fetchone(), in_app_db)
    return real_project_data

def get_releases(in_app_db, project_id: str) -> dict:
    """Returns a list of releases for a given project ID."""
    with DatabaseContext(in_app_db, cursor_factory=RealDictCursor) as cur:
        comm = SQL("select * from Release where projectId = %s")
        cur.execute(comm, [project_id])
        return cur.fetchall()

def get_screenshots(in_app_db, project_id: str) -> list:
    with DatabaseContext(in_app_db, cursor_factory=RealDictCursor) as cur:
        comm = SQL("select screenUrl from Screenshot where projectId = %s")
        cur.execute(comm, [project_id])
        screens_data = cur.fetchall()
    return [s["screenurl"] for s in screens_data]

def get_reviews(in_app_db, project_id: str) -> dict:
    """Returns reviews for a given project"""
    with DatabaseContext(in_app_db, cursor_factory=RealDictCursor) as cur:
        comm = SQL("select * from Reviews where projectId = %s")
        cur.execute(comm, [project_id])
        return cur.fetchall()

def get_reviews_by_user(in_app_db, userId: str) -> dict:
    """Returns all reviews that the user made"""
    with DatabaseContext(in_app_db, cursor_factory=RealDictCursor) as cur:
        comm = SQL("select * from Reviews where userId = %s")
        cur.execute(comm, [userId])
        return cur.fetchall()

def get_dependencies(in_app_db, project_id: str) -> dict:
    """Returns all dependencies of a given project"""
    with DatabaseContext(in_app_db, cursor_factory=RealDictCursor) as cur:
        comm = SQL("select * from (DependsOn natural join Project) where projectId = %s")
        cur.execute(comm, [project_id])
        return cur.fetchall()

def get_project_license(in_app_db, license_id) -> Optional[str]:
    with DatabaseContext(in_app_db, cursor_factory=RealDictCursor) as cursor:
        command = SQL("select licenseName from License where licenseId = %s")
        cursor.execute(command, [license_id])
        result = cursor.fetchone()

    if not result:
        return None
    return result["licensename"]

def get_project_permissions(in_app_db, project_id: str) -> list:
    with DatabaseContext(in_app_db, cursor_factory=RealDictCursor) as cursor:
        command = SQL("select requiredKey from Requires where projectId = %s")
        cursor.execute(command, [project_id])
        return [req["requiredkey"] for req in cursor.fetchall()]

def get_permission(in_app_db, perm: str) -> dict:
    with DatabaseContext(in_app_db, cursor_factory=RealDictCursor) as cursor:
        command = SQL("select * from Permission where requiredKey = %s")
        cursor.execute(command, [perm])
        return cursor.fetchone()

def get_projects_by_developer(in_app_db, userId: str) -> list:
    """Returns all the projects for a developer"""
    with DatabaseContext(in_app_db, cursor_factory = RealDictCursor) as cur:
        comm = SQL("select * from (Maintains natural join Project) where userId = %s")
        cur.execute(comm, [userId])
        projects = []
        for project in cur.fetchall():
            projects.append(__transform_project_data(project, in_app_db))
        return projects

def get_developer(in_app_db, of_project_id: str) -> dict:
    with DatabaseContext(in_app_db, cursor_factory=RealDictCursor) as cursor:
        command = SQL("select userId, name from (Maintains natural join Account) where projectId = %s")
        cursor.execute(command, [of_project_id])
        return cursor.fetchone()
