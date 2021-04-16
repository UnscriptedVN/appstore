# appdb.py
# (C) 2021 Marquis Kurt, Nodar Sotkilava, and Unscripted VN Team.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from flask import Flask, render_template, jsonify
from . import roland as ro
import sys

app = Flask(__name__)
app.config.from_pyfile("config.py")
app.config['DEBUG'] = True

APPDB_CONNECTION = None

try:
    APPDB_CONNECTION = ro.utils.load_database(app.config)
except Exception as error:
    print(error, file=sys.stderr)

###########################################
# MARK: API ENDPOINTS                     #
###########################################
# TODO: Determine if it's possible to move these to their own files...

@app.route("/api/v1/authenticate")
def authenticate():
    # FIXME: Implement user authentication with GitHub.
    return jsonify({ "error": "Not implemented "}), 500

@app.route("/api/v1/projects/<string:id>")
def api_single_project(id: str):
    project = ro.projects.get_project(APPDB_CONNECTION, id)
    if not project:
        return jsonify({"error": "Record not found"}), 404
    return jsonify(project)

@app.route("/api/v1/projects/<string:id>/releases")
def api_project_releases(id: str):
    project = ro.projects.get_project(APPDB_CONNECTION, id)
    if not project:
        return jsonify({"error": "Record not found"}), 404
    
    releases = ro.projects.get_releases(APPDB_CONNECTION, id)
    return jsonify(releases)

@app.route("/api/v1/projects", methods=['GET'])
def api_get_project():
    return jsonify(ro.projects.list_projects(APPDB_CONNECTION))

@app.route("/api/v1/search")
def api_search():
    return ro.search.search(APPDB_CONNECTION)

###########################################
# MARK: ERROR HANDLING                    #
###########################################

@app.errorhandler(404)
def page_not_found(e):
    return render_template("pages/error.html", errcode=404), 404

if not app.config['DEBUG']:
    @app.errorhandler(Exception)
    def internal_server_error(e):
        print(e, file=sys.stderr)
        return render_template("pages/error.html", errcode=500), 500

###########################################
# MARK: USER PAGES                        #
###########################################

@app.route("/")
def index():
    return "200", 200

@app.route("/apps")
def prod_apps():
    return "200", 200

@app.route("/lists")
def prod_lists():
    return "200", 200

@app.route("/search")
def prod_search():
    return "200", 200


@app.route("/auth/login")
def auth_login():
    return "200", 200


@app.route("/auth/logout")
def auth_logout():
    return "200", 200

###########################################
# MARK: DEVELOPER PAGES                   #
###########################################

@app.route("/developer/dashboard")
def dev_dashboard():
    return "200", 200

###########################################
# MARK: CURATOR PAGES                     #
###########################################

@app.route("/curator/dashboard")
def cur_dashboard():
    return "200", 200

if __name__ != "__main__":
    application = app
