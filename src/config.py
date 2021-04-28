# config.py
# (C) 2021 Marquis Kurt, Nodar Sotkilava, and Unscripted VN Team.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from os import getenv
from dotenv import load_dotenv
from json import load

load_dotenv(".env")

# PostgreSQL environment variables
PSQL_USER = getenv("PSQL_USER")
PSQL_PWD = getenv("PSQL_PWD")
PSQL_DB = getenv("PSQL_DB")
PSQL_HOST = getenv("PSQL_HOST")

# GitHub API variables
GH_CLIENT_ID = getenv("GH_CLIENT_ID")
GH_CLIENT_SECRET = getenv("GH_CLIENT_SECRET")

# Frontpage configuration
with open("frontpage.json", "r") as config_file:
    FRONTPAGE_CONFIG = load(config_file)

if not FRONTPAGE_CONFIG:
    FRONTPAGE_CONFIG = {}

if "featured_project" not in FRONTPAGE_CONFIG:
    FRONTPAGE_CONFIG["featured_project"] = None

if "featured_lists" not in FRONTPAGE_CONFIG:
    FRONTPAGE_CONFIG["featured_lists"] = []

SECRET_KEY = "cnh3X2lkZW50aWZpZWRfY2VydGlmaWNhdGUK"