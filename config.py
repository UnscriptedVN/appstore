# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from os import getenv
from dotenv import load_dotenv

load_dotenv(".env")

# PostgreSQL environment variables
PSQL_USER = getenv("PSQL_USER")
PSQL_PWD = getenv("PSQL_PWD")

# GitHub API variables
GH_CLIENT_ID = getenv("GH_CLIENT_ID")
GH_CLIENT_SECRET = getenv("GH_CLIENT_SECRET")