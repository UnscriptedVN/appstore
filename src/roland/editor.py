# editor.py
# (C) 2021 Marquis Kurt, Nodar Sotkilava, and Unscripted VN Team.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https: //mozilla.org/MPL/2.0/.

from psycopg2.sql import SQL
from .projects import ProjectType, get_project, get_project_permissions
from .utils import DatabaseContext

def create_project(
    in_app_db, from_developer_id: int, name: str, identifier: str, type: ProjectType, tagline: str, license: int = 1):
    """Create a releasable project in the database.
    
    Arguments:
        in_app_db: The database connection that will be used to make the project.
        from_developer_id: The developer's ID that will be associated with this project.
        name: The name of the project.
        identifier: The immutable, uniquely-identifying project identifier for this new project.
        type: The type of project to create.
        tagline: A short description of the project.
        license: The ID of the license the project resides under. Defaults to proprietary.
    """
    with DatabaseContext(in_app_db) as cursor:
        new_app_command = SQL("insert into Project values (%s, %s, %s, '0.0.0', %s, null, %s, null)")
        cursor.execute(new_app_command, [identifier, type.value, name, tagline, license])

        link_to_developer_command = SQL("insert into Maintains values (%s, %s)")
        cursor.execute(link_to_developer_command, [identifier, from_developer_id])
        in_app_db.commit()

def update_project_licensing(in_app_db, project_id: str, license: int = 1):
    """Update the license for a project.
    
    Arguments:
        in_app_db: The database connection that will be used to update the licensing.
        project_id: The project whose license will be updated.
        license: The ID of the license in the AppDB database.
    """
    with DatabaseContext(in_app_db) as cursor:
        command = SQL("update Project set licenseId = %s where projectId = %s")
        cursor.execute(command, [license, project_id])
        in_app_db.commit()

def update_project_icon(in_app_db, project_id: str, icon_url: str):
    """Update the icon for a project.

    Arguments:
        in_app_db: The database connection that will be used to update the icon.
        project_id: The project whose icon will be updated.
        icon_url: A URL pointing to the project's icon.
    """
    with DatabaseContext(in_app_db) as cursor:
        command = SQL("update Project set projectIcon = %s where projectId = %s")
        cursor.execute(command, [icon_url, project_id])
        in_app_db.commit()

def update_project_metadata(in_app_db, project_id: str, **kwargs):
    """Update the project's metadata.

    Arguments:
        in_app_db: The database connection that will be used to update the properties of the project.
        project_id: The project whose metadata will be updated.
        **kwargs: Arbitrary keyword arguments.
    """
    current = get_project(in_app_db, project_id)
    if not current:
        raise KeyError
    
    new_name = kwargs["name"] if "name" in kwargs else current["name"]
    new_desc = kwargs["description"] if "description" in kwargs else current["description"]
    new_blurb = kwargs["blurb"] if "blurb" in kwargs else current["blurb"]

    with DatabaseContext(in_app_db) as cursor:
        command = SQL("update Project set name = %s, description = %s, blurb = %s where projectId = %s")
        cursor.execute(command, [new_name, new_desc, new_blurb, project_id])
        in_app_db.commit()

def update_project_permission(in_app_db, project_id: str, permission_key: str, mode="add"):
    """Declare or remove a permission from a project.

    If the database does not have a row containing the project ID and the permission key in the Requires table, it will
        be created. Otherwise, the row will be deleted from the table.
    
    Arguments:
        in_app_db: The database connection that will be used to update the permission for the project.
        project_id: The project whose permissions will be updated.
        permission_key: The permission to add or remove from the project.
    """
    existing_perms = get_project_permissions(in_app_db, project_id)

    if mode == "remove" and permission_key not in existing_perms:
        return

    if permission_key in existing_perms and mode == "remove":
        with DatabaseContext(in_app_db) as cursor:
            command = SQL("delete from Requires where projectId = %s and requiredKey = %s")
            cursor.execute(command, [project_id, permission_key])
            in_app_db.commit()
            return
    
    if permission_key in existing_perms and mode == "add":
        return

    with DatabaseContext(in_app_db) as cursor:
        command = SQL("insert into Requires values (%s, %s)")
        cursor.execute(command, [project_id, permission_key])
        in_app_db.commit()


def update_project_permissions(in_app_db, project_id: str, added, removed):
    """Update a project's permission list using a list of added and removed permissions."""
    for permission in added:
        update_project_permission(in_app_db, project_id, permission, mode="add")
    for permission2 in removed:
        update_project_permission(in_app_db, project_id, permission2, mode="remove")


def delete_project(in_app_db, project_id: str):
    with DatabaseContext(in_app_db) as cursor:
        # Delete any Action Center messages with this project.
        delete_messages = SQL("delete from Message where projectId = %s")
        cursor.execute(delete_messages, [project_id])
        
        # Delete the releases for this project.
        delete_releases = SQL("delete from Release where projectId = %s")
        cursor.execute(delete_releases, [project_id])

        # Delete the releases for this project.
        delete_reviews = SQL("delete from Reviews where projectId = %s")
        cursor.execute(delete_reviews, [project_id])

        # Delete the permissions for this project.
        delete_permissions = SQL("delete from Requires where projectId = %s")
        cursor.execute(delete_permissions, [project_id])

        # Delete the maintainership role.
        delete_maintainership = SQL("delete from Maintains where projectId = %s")
        cursor.execute(delete_maintainership, [project_id])

        # Delete the screenshots.
        delete_screenshots = SQL("delete from Screenshot where projectId = %s")
        cursor.execute(delete_screenshots, [project_id])

        # Remove the app from any lists.
        delete_inclusion = SQL("delete from Includes where projectId = %s")
        cursor.execute(delete_inclusion, [project_id])

        # Finally, delete the project itself.
        delete_project = SQL("delete from Project where projectId = %s")
        cursor.execute(delete_project, [project_id])
        in_app_db.commit()
