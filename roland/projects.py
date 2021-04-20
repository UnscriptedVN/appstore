# projects.py
# (C) 2021 Marquis Kurt, Nodar Sotkilava, and Unscripted VN Team.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from .utils import DatabaseContext
from psycopg2.extras import RealDictCursor, RealDictRow
from psycopg2.sql import SQL
from enum import IntEnum

class ProjectType(IntEnum):
    """An enum that represents the different project types."""
    App = 0
    CoreService = 1
    Framework = 2


def __transform_project_data(project: RealDictRow) -> RealDictRow:
    """Returns a transformed version of the project data, or itself if the project doesn't exist."""
    if not project:
        return project
    new_project = project.copy()
    
    new_project["id"] = new_project["projectid"]
    del new_project["projectid"]
    
    new_project["latest_version"] = new_project["version"]
    del new_project["version"]
    
    new_project["license"] = new_project["licenseid"]
    del new_project["licenseid"]
    
    new_project["icon"] = new_project["projecticon"]
    del new_project["projecticon"]
    
    new_project["type"] = str(ProjectType(new_project["type"]).name).lower()
    return new_project

def list_projects(in_app_db) -> list:
    """Returns a list of all projects."""
    with DatabaseContext(in_app_db, cursor_factory=RealDictCursor) as cur:
        cur.execute('select * from Project')
        data = cur.fetchall().copy()
    projects = []
    for project in data:
        new_project = __transform_project_data(project)
        new_project["releases"] = get_releases(in_app_db, project["projectid"])
        new_project["screenshots"] = get_screenshots(in_app_db, project["projectid"])
        projects.append(new_project)
    return projects

def get_project(in_app_db, project_id: str) -> dict:
    """Returns the row in the projects table with a specified ID."""
    with DatabaseContext(in_app_db, cursor_factory=RealDictCursor) as cur:
        comm = SQL("select * from Project where projectid = %s")
        cur.execute(comm, [project_id])
        real_project_data = __transform_project_data(cur.fetchone())
    real_project_data["releases"] = get_releases(in_app_db, project_id)
    real_project_data["screenshots"] = get_screenshots(in_app_db, project_id)
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

def get_permissions(in_app_db, project_id: str) -> dict:
    """Returns all the system permissions required by the project """
    with DatabaseContext(in_app_db, cursor_factory=RealDictCursor) as cur:
        comm = SQL("select * from (Requires natural join Permission) where projectId = %s")
        cur.execute(comm, [project_id])
        return cur.fetchall()

def get_projects_by_developer(in_app_db, userId: str) -> dict:
    """Returns all the projects for a developer"""
    with DatabaseContext(in_app_db, cursor_factory = RealDictCursor) as cur:
        comm = SQL("select * from (Mantains natural join Project) where userId = %s")
        cur.execute(comm, [userId])
        return cur.fetchall()