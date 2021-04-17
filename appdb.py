# appdb.py
# (C) 2021 Marquis Kurt, Nodar Sotkilava, and Unscripted VN Team.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from flask import Flask, render_template, jsonify, request, redirect, abort
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

@app.route("/api/v1/authenticate", methods=["GET"])
def authenticate():
    # FIXME: Implement user authentication with GitHub.
    query = request.args

    if query.get("error"):
        return jsonify({ 
            "error": "GitHub Authorization Failure",
            "details": query.get("error_description")
        }), 400

    return jsonify({ "error": "Not implemented "}), 500

@app.route("/api/v1/projects/<string:id>", methods=["GET"])
def api_single_project(id: str):
    project = ro.projects.get_project(APPDB_CONNECTION, id)
    if not project:
        return jsonify({"error": "Record not found"}), 404
    return jsonify(project)

@app.route("/api/v1/projects/<string:id>/releases", methods=["GET"])
def api_project_releases(id: str):
    project = ro.projects.get_project(APPDB_CONNECTION, id)
    if not project:
        return jsonify({"error": "Record not found"}), 404
    
    releases = ro.projects.get_releases(APPDB_CONNECTION, id)
    return jsonify(releases)

@app.route("/api/v1/projects", methods=['GET'])
def api_get_project():
    return jsonify(ro.projects.list_projects(APPDB_CONNECTION))

@app.route("/api/v1/search", methods=["GET"])
def api_search():
    return ro.search.search(APPDB_CONNECTION)

@app.route("/api/v1/users/<string:id>", methods = ['GET'])
def api_get_user(id: str):
    return jsonify(ro.accounts.get_account(APPDB_CONNECTION, id))

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
    featured = ro.projects.get_project(
        APPDB_CONNECTION, "dev.unscriptedvn.candella.celeste-shell")
    return render_template("pages/index.html", featured=featured), 200

@app.route("/apps")
def prod_apps():
    # FIXME: Implement this page.
    abort(404)

@app.route("/lists")
def prod_lists():
    # FIXME: Implement this page.
    abort(404)

@app.route("/search")
def prod_search():
    # FIXME: Implement this page.
    abort(404)


@app.route("/apps/<string:project_id>")
def project_detail(project_id):
    return abort(404)


@app.route("/auth/login")
def auth_login():
    client_id = app.config['GH_CLIENT_ID']
    auth_url = f"https://github.com/login/oauth/authorize?client_id={client_id}"\
        + "&scope=user:email%20read:user&allow_signup=true"
    return render_template("pages/login.html", gh_auth_url=auth_url), 200


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
