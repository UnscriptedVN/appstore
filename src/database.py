# database.py
# (C) 2021 Marquis Kurt, Nodar Sotkilava, and Unscripted VN Team.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https: //mozilla.org/MPL/2.0/.

from flask import g as gblspace, current_app
from . import roland as ro


def connect_database():
    if "database" not in gblspace:
        gblspace.database = ro.utils.load_database(current_app.config)
    return gblspace.database


def close_database():
    database = gblspace.pop("database", None)
    if database is not None:
        database.close()


def frontpage_config() -> dict:
    if "frontpage" not in gblspace:
        gblspace.frontpage = current_app.config["FRONTPAGE_CONFIG"]
    return gblspace.frontpage


def pop_frontpage():
    gblspace.pop("frontpage", None)

