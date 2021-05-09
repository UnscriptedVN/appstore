# accounts.py
# (C) 2021 Marquis Kurt, Nodar Sotkilava, and Unscripted VN Team.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from .utils import DatabaseContext
from psycopg2.extras import RealDictCursor, RealDictRow
from psycopg2.sql import SQL
from enum import IntEnum
from typing import Optional, Dict


class AccountType(IntEnum):
    """An enum that represents the diffrent account types."""
    UserAccount = 0
    Developer = 1
    Curator = 2


def __get_account_type(account: RealDictRow) -> RealDictRow:
    """Return an account type"""
    if not account:
        return account
    new_account = account.copy()

    new_account["type"] = str(AccountType(
        new_account["accounttype"]).name).lower()

    return new_account


def get_account_by_email(in_app_db, email: str) -> dict:
    """Returns the row in the accounts projects table with a specified email."""
    with DatabaseContext(in_app_db, cursor_factory=RealDictCursor) as cur:
        comm = SQL("select * from Account where email = %s")
        cur.execute(comm, [email])
        account = __get_account_type(cur.fetchone())
        return account


def get_account(in_app_db, userId: int) -> dict:
    """Returns the row in the accounts projects table with a specified ID."""
    with DatabaseContext(in_app_db, cursor_factory=RealDictCursor) as cur:
        comm = SQL("select * from Account where userId = %s")
        cur.execute(comm, [userId])
        account = __get_account_type(cur.fetchone())
        return account


def get_account_by_github_id(in_app_db, gh_id: str) -> Optional[RealDictRow]:
    with DatabaseContext(in_app_db, cursor_factory=RealDictCursor) as cur:
        comm = SQL("select * from Account where githubId = %s")
        cur.execute(comm, [str(gh_id)])
        return cur.fetchone()


def create_account(in_app_db, username, email_address, github_id, type=AccountType.UserAccount):
    """Creates an account on the database."""
    with DatabaseContext(in_app_db) as cursor:
        command = SQL(
            "insert into Account (githubId, name, email, accountType) values (%s, %s, %s, %s)")
        cursor.execute(
            command, [str(github_id), username, email_address, type])
        in_app_db.commit()
    return get_account_by_github_id(in_app_db, github_id)


def update_account_type(in_app_db, user_id, account_type=AccountType.UserAccount):
    """Update the type of account present."""
    with DatabaseContext(in_app_db) as cursor:
        command = SQL("update Account set accountType = %s where userId = %s")
        cursor.execute(command, [account_type, user_id])
        in_app_db.commit()
        
def update_user_settings(in_app_db, user_id, email, name):
    """Update the settings in the user account"""
    with DatabaseContext(in_app_db) as cursor:
        if email:
            command = SQL("update Account set email = %s where userId = %s")
            cursor.execute(command, [email, user_id])
        if name: 
            command = SQL("update Account set name = %s where userId = %s")
            cursor.execute(command, [name, user_id])
        in_app_db.commit()

def delete_user(in_app_db, user_id, account_type):
    #Not pretty but that's for future randy to worry about
    """Delete the account and everything associated with it."""
     with DatabaseContext(in_app_db) as cursor:
        command = SQL("delete from Account where userId = %s")
        cursor.execute(command, [user_id])
        command = SQL("delete from (Project natural join Maintains) where userId = %s")
        cursor.execute(command, [user_id])
        command = SQL("delete from Reviews where userId = %s")
        cursor.execute(command, [user_id])
        if account_type == AccountType.Curator:
            command = SQL("delete from List where userId = %s")
            cursor.execute(command, [user_id])
        #More to be added??
        in_app_db.commit()
        