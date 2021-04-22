# config.py
# (C) 2021 Marquis Kurt, Nodar Sotkilava, and Unscripted VN Team.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from os import getenv, urandom
from dotenv import load_dotenv

load_dotenv(".env")

# PostgreSQL environment variables
PSQL_USER = getenv("PSQL_USER")
PSQL_PWD = getenv("PSQL_PWD")
PSQL_DB = getenv("PSQL_DB")
PSQL_HOST = getenv("PSQL_HOST")

# GitHub API variables
GH_CLIENT_ID = getenv("GH_CLIENT_ID")
GH_CLIENT_SECRET = getenv("GH_CLIENT_SECRET")

SECRET_KEY = urandom(16)