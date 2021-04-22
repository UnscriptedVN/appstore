# developer.py
# (C) 2021 Marquis Kurt, Nodar Sotkilava, and Unscripted VN Team.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https: //mozilla.org/MPL/2.0/.

from flask import Blueprint, abort, session
from .database import connect_database
from . import roland as ro

developer = Blueprint("developer", __name__, template_folder="../templates", static_folder="../static", url_prefix="/developer")

@developer.route("/dashboard")
def dev_dashboard():
    acct = ro.accounts.get_account(connect_database(), session.get("cuid"))
    if not acct or acct["accounttype"] != ro.accounts.AccountType.Developer:
        abort(401)
    return "200", 200
