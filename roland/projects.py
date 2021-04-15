# projects.py
# (C) 2021 Marquis Kurt, Nodar Sotkilava, and Unscripted VN Team.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from . import utils
from psycopg2.extras import RealDictCursor

def get_projects(in_app_db, **kwargs) -> dict:
    """Returns a list of all projects, given a specific criteria."""
    with utils.DatabaseContext(in_app_db, cursor_factory=RealDictCursor) as cur:
        cur.execute('select * from Project')
        return cur.fetchall()
