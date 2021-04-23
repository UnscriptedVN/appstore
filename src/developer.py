# developer.py
# (C) 2021 Marquis Kurt, Nodar Sotkilava, and Unscripted VN Team.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https: //mozilla.org/MPL/2.0/.

from sys import stderr
from flask import Blueprint, abort, session, render_template, request, jsonify, url_for, redirect
from .database import connect_database
from . import roland as ro

developer = Blueprint(
    "developer", __name__, template_folder="../templates", static_folder="../static", url_prefix="/developer")

def __verify_developer():
    """Verify that the account has at least developer permissions to view.
    
    NOTE: In the future, this might want to be changed so that curators don't have access to these pages as well, though
        this may conflict with the Unscripted VN Team's official development projects.
    """
    acct = ro.accounts.get_account(connect_database(), session.get("cuid"))
    if not acct or acct["accounttype"] == ro.accounts.AccountType.UserAccount:
        abort(401)
    return acct

@developer.route("/dashboard")
def dev_dashboard():
    acct = __verify_developer()
    dev_projects = ro.projects.get_projects_by_developer(connect_database(), acct["userid"])
    return render_template("pages/developer/dashboard.html", developer=acct, projects=dev_projects, action="manage"), 200

@developer.route("/projects/create")
def create_project():
    __verify_developer()
    return render_template("pages/developer/project_wizard.html"), 200

@developer.route("/projects/new", methods=["GET", "POST"])
def create_project_request():
    __verify_developer()
    if not request.form:
        abort(400)
    for keys in request.form:
        if keys in ["name", "id", "blurb"] and not request.form[keys]:
            abort(400)
    try:
        ro.editor.create_project(
            connect_database(), session.get('cuid'), request.form["name"], request.form["id"],
            ro.projects.ProjectType(int(request.form["type"])), request.form["blurb"])
        return redirect(url_for("developer.edit_project", id=request.form["id"]))
    except Exception as error:
        print(error, stderr)
        abort(500)

@developer.route("/projects/<string:id>")
@developer.route("/projects/<string:id>/info")
def edit_project(id: str):
    project = ro.projects.get_project(connect_database(), id)
    licenses = ro.licensing.get_all_licenses(connect_database())
    if not project:
        abort(500)
    return render_template("pages/developer/project_editor.html", project=project, licenses=licenses, tab="info"), 200


@developer.route("/projects/<string:id>/releases")
def edit_project_releases(id: str):
    project = ro.projects.get_project(connect_database(), id)
    if not project:
        abort(500)
    return render_template("pages/developer/project_editor.html", project=project, tab="releases"), 200

@developer.route("/projects/<string:id>/messages")
def edit_project_messages(id: str):
    project = ro.projects.get_project(connect_database(), id)
    if not project:
        abort(500)
    return render_template("pages/developer/project_editor.html", project=project, tab="messages"), 200


@developer.route("/projects/<string:id>/reviews")
def edit_project_reviews(id: str):
    project = ro.projects.get_project(connect_database(), id)
    if not project:
        abort(500)
    return render_template("pages/developer/project_editor.html", project=project, tab="reviews"), 200


@developer.route("/projects/update_information", methods=["GET", "POST"])
def update_project_information():
    if not request.form:
        abort(400)
    
    for nonempty_key in request.form:
        if nonempty_key in ["name", "description", "id"] and not request.form[nonempty_key]:
            abort(400)
    
    proj_id = request.form["id"]

    try:
        ro.editor.update_project_icon(connect_database(), proj_id, request.form["icon"])
        ro.editor.update_project_licensing(connect_database(), proj_id, int(request.form["license"]))
        ro.editor.update_project_metadata(
            connect_database(), proj_id, name=request.form["name"], description=request.form["description"], 
            blurb=request.form["blurb"])
        return redirect(url_for('developer.edit_project', id=request.form['id']))
    except Exception as error:
        print(error, stderr)
        abort(500)

    return "200", 200