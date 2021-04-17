# auth.py
# (C) 2021 Marquis Kurt, Nodar Sotkilava, and Unscripted VN Team.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https: //mozilla.org/MPL/2.0/.

from flask import request

def authenticate_with_github(temporary_code, **kwargs):
    """Attempt to authenticate with GitHub using the temporary code."""
    if "client_id" not in kwargs or "client_secret" not in kwargs:
        raise PermissionError("Cannot authenticate to GitHub with empty client information.")
    


def authenticated() -> bool:
    """Returns whether the user is authenticated."""
    # FIXME: Implement this method.
    return False