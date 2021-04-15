# appdb.py
# (C) 2021 Marquis Kurt, Nodar Sotkilava, and Unscripted VN Team.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from flask import Flask, render_template, json, session, request, jsonify
import psycopg2 as psql
import psycopg2.extras as psql_extras
import sys
import psycopg2.extensions as psql_ext
from . import roland as ro

app = Flask(__name__)
app.config.from_pyfile("config.py")
app.config['DEBUG'] = True

#Establish connection to the DB
APPDB_CONNECTION = None
try:
    APPDB_CONNECTION = ro.utils.load_database(app.config)
except psql.DatabaseError as error:
    print(error, file = sys.stderr)

# TODO: Add routes here

#Returns 404 if something goes wrong
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

#Returns OK if connected
@app.route("/")
def connect():
    return "200", 200

#SELECT all the projects from Project
# NOTE: This endpoint should probably be changed to just "/api/v1/projects".
@app.route("/api/v1/projects/all", methods = ['GET'])
def projects():
    return jsonify(ro.projects.get_projects(APPDB_CONNECTION))

@app.route("/api/v1/project/<string:id>")
def single_project(id: str):
    return jsonify(ro.projects.get_project(APPDB_CONNECTION, id))

@app.route("/api/v1/search")
def search_database():
    return ro.search.search(APPDB_CONNECTION)

#SELECTs a specific project based on the parameters passed
# NOTE: This endpoint should probably be removed or integrated into a general search API
# call.
@app.route("/api/v1/projects", methods = ['GET'])
def get_project():
    return jsonify(ro.projects.get_projects(APPDB_CONNECTION))

if __name__ != "__main__":
    application = app
