# auth.py
# (C) 2021 Marquis Kurt, Nodar Sotkilava, and Unscripted VN Team.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https: //mozilla.org/MPL/2.0/.

from flask import request, session
from .utils import DatabaseContext
from .accounts import get_account, get_account_by_email
from passlib.hash import pbkdf2_sha256

def authenticate_with_github(temporary_code, **kwargs):
    """Attempt to authenticate with GitHub using the temporary code."""
    if "client_id" not in kwargs or "client_secret" not in kwargs:
        raise PermissionError("Cannot authenticate to GitHub with empty client information.")
    
    # FIXME: Make POST request to GitHub API here to get the GH access token.

    # If the login is successful, set cuid and login_token to the auth_token.
    account = get_account_by_email(kwargs["app_database"], "github_email")
    if account:
        session["cuid"] = account["id"]
        session["login_token"] = auth_token(0, account["email"], account["name"])
        session.changed = True
    else:
        # FIXME: Redirect to the registration process.
        pass



def authenticated(with_app_db) -> bool:
    """Returns whether the user is authenticated."""

    # Check that we have stored a token and current user ID in the session storage.
    token, cuid = session.get("login_token"), session.get("cuid")
    if not token or not cuid:
        return False

    # Fetch the user data from the database. If this user doesn't exist, return false.
    user_account = get_account(with_app_db, cuid)
    if not user_account:
        return False

    # Compare the user data to the token in the session storage.
    email, name = user_account["email"], user_account["name"]
    return pbkdf2_sha256.verify(token, auth_token(cuid, email, name))



def auth_token(user_id, user_email, user_name) -> str:
    """Returns an authentication token based on the format of the DB."""
    return pbkdf2_sha256.hash(f"{user_id}:{user_email}:{user_name}")
