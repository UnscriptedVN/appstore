# appdb.py
# (C) 2021 Marquis Kurt, Nodar Sotkilava, and Unscripted VN Team.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from flask import Flask, render_template, jsonify, request, redirect, abort, session
from flask.helpers import url_for
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
    query = request.args
    if query.get("error") or not query.get("code"):
        return jsonify({
            "error": "GitHub authorization failed."
        }), 400
    try:
        redirect_to = ro.auth.authenticate_with_github(
            query.get("code"),
            client_id=app.config["GH_CLIENT_ID"],
            client_secret=app.config["GH_CLIENT_SECRET"],
            app_database=APPDB_CONNECTION)
        return redirect(url_for("auth_register")) if redirect_to == "registered" else redirect(url_for("index"))
    except Exception as error:
        print(error, file=sys.stderr)
        abort(500)


@app.route("/api/v1/projects/<string:id>", methods=["GET"])
def api_single_project(id: str):
    project = ro.projects.get_project(APPDB_CONNECTION, id)
    if not project:
        return jsonify({"error": "Record not found"}), 404
    return jsonify(project)

@app.route("/api/v1/projects/<string:id>/releases", methods = ['GET'])
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


@app.route("/api/v1/users/<int:id>", methods = ['GET'])
def api_get_user(id: int):
   account = ro.accounts.get_account(APPDB_CONNECTION, id)
   if not account:
       return jsonify({"error": "Record not found"}), 404
   return jsonify(account)

@app.route("/api/v1/lists", methods = ["GET"])
def api_get_all_lists():
    return jsonify(ro.lists.get_all_curator_lists(APPDB_CONNECTION))

@app.route("/api/v1/lists/<string:id>", methods = ['GET'])
def api_single_list(id: str):
    return jsonify(ro.lists.get_one_list(APPDB_CONNECTION, id))

@app.route("/api/v1/lists/curator/<string:id>", methods = ['GET'])
def api_curator_lists(id:str):
    return jsonify(ro.lists.get_curator_lists(APPDB_CONNECTION, id))

@app.route("/api/v1/lists/project/<string:id>", methods = ['GET'])
def api_get_project_in_curator_list(id:str):
    return jsonify(ro.lists.get_project_in_curator_list(APPDB_CONNECTION, id))

###########################################
# MARK: ERROR HANDLING                    #
###########################################
def __database_failure():
    return render_template("pages/dbsetup.html"), 500

@app.errorhandler(404)
def err_page_not_found(e):
    return render_template("pages/error.html", errcode=404), 404

@app.errorhandler(401)
def err_forbidden(e):
    return render_template("pages/error.html", errcode=401), 401

@app.errorhandler(500)
def err_internal_server(e):
    return render_template("pages/error.html", errcode=500), 500


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
    if not APPDB_CONNECTION:
        return __database_failure()
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
    app = ro.projects.get_project(APPDB_CONNECTION, project_id)
    if not app:
        abort(404)
    
    permissions = [] if not app["permissions"] else \
        [ro.projects.get_permission(APPDB_CONNECTION, val) for val in app["permissions"]]

    developer = ro.projects.get_developer(APPDB_CONNECTION, app["id"])
    related = ro.projects.get_projects_by_developer(APPDB_CONNECTION, developer["userid"])

    return render_template(
        "pages/app_detail.html", app=app, permissions=permissions, dev=developer, rel=related), 200

@app.route("/apps/developer/<int:developer_id>")
def developer_detail(developer_id: int):
    # TODO: Return a page instead of the raw data.
    developer = ro.accounts.get_account(APPDB_CONNECTION, developer_id)
    if not developer:
        abort(404)
    if developer["accounttype"] != ro.accounts.AccountType.Developer:
        abort(500)

    projects_by_dev = ro.projects.get_projects_by_developer(APPDB_CONNECTION, developer["userid"])
    return render_template("pages/dev_detail.html", developer=developer, projects=projects_by_dev), 200

###########################################
# MARK: AUTHENTICATION PAGES              #
###########################################

@app.route("/auth/register")
def auth_register():
    if not APPDB_CONNECTION:
        return __database_failure()
    if not session.get("rxw_reg"):
        abort(401)
    new_account = ro.accounts.get_account(APPDB_CONNECTION, session["cuid"])
    session.modified = True
    return render_template("pages/acct_register.html", account=new_account), 200


@app.route("/auth/register/callback", methods=["GET", "POST"])
def update_account_type():
    if not session.get("rxw_reg") or not session.get("login_token"):
        abort(401)
    account_type = ro.accounts.AccountType(int(request.form["account_type"]))
    ro.accounts.update_account_type(APPDB_CONNECTION, session.get("cuid"), account_type=account_type)
    del session["rxw_reg"]
    return redirect(url_for("index"))

@app.route("/auth/login")
def auth_login():
    if not APPDB_CONNECTION:
        return __database_failure()
    if session.get("cuid") or session.get("login_token"):
        return redirect(url_for("auth_register")) if session["rxw_reg"] else redirect(url_for("index"))
    client_id = app.config['GH_CLIENT_ID']
    auth_url = f"https://github.com/login/oauth/authorize?client_id={client_id}"\
        + "&scope=user:email%20read:user&allow_signup=true"
    return render_template("pages/login.html", gh_auth_url=auth_url), 200


@app.route("/auth/logout")
def auth_logout():
    if session.get("cuid"):
        del session["cuid"]
    if session.get("login_token"):
        del session["login_token"]
    session.modified = True
    return redirect(url_for("index"))

###########################################
# MARK: DEVELOPER PAGES                   #
###########################################


@app.route("/developer/dashboard")
def dev_dashboard():
    acct = ro.accounts.get_account(APPDB_CONNECTION, session.get("cuid"))
    if not acct or acct["accounttype"] != ro.accounts.AccountType.Developer:
        abort(401)
    return "200", 200

###########################################
# MARK: CURATOR PAGES                     #
###########################################


@app.route("/curator/dashboard")
def cur_dashboard():
    acct = ro.accounts.get_account(APPDB_CONNECTION, session.get("cuid"))
    if not acct or acct["accounttype"] != ro.accounts.AccountType.Curator:
        abort(401)
    return "200", 200


if __name__ != "__main__":
    application = app
