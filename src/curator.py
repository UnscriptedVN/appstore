# curator.py
# (C) 2021 Marquis Kurt, Nodar Sotkilava, and Unscripted VN Team.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https: //mozilla.org/MPL/2.0/.

from flask import Blueprint, render_template, jsonify, request, abort, session
from flask.helpers import url_for
from werkzeug.utils import redirect
from .database import connect_database
from . import roland as ro

curator = Blueprint("curator", __name__, template_folder="../templates", static_folder="../static", url_prefix="/curator")

def _verify_curator():
    """Verify that the currently logged-in user is indeed a curator."""
    acct = ro.accounts.get_account(connect_database(), session.get("cuid"))
    if not acct or acct["accounttype"] != ro.accounts.AccountType.Curator:
        abort(401)
    return acct

@curator.route("/dashboard")
def cur_dashboard():
    account = _verify_curator()
    ###THIS IS FOR TESTING!!!!
    ro.releases.assign_release(connect_database(),"dev.unscriptedvn.candella.celeste-shell","1", int(session.get("cuid")))
    ###REMOVE BEFORE RELEASE!!!
    pending_release = ro.releases.get_pending_releases(connect_database())
    pending_release_names = {}
    if (pending_release):
        pending_release = [release for release in pending_release if account["userid"] == release["userid"]]
        for release in pending_release:
            pending_release_names[release["projectid"]] = ro.projects.get_project(connect_database(), release["projectid"])["name"]
    return render_template("pages/curator/dashboard.html", curator=account, projects = pending_release, action = "review", pending_release_names = pending_release_names), 200

@curator.route("/lists")
def lists_dashboard():
    _verify_curator()
    cur_lists = ro.lists.get_curator_lists(connect_database(), session.get("cuid"))
    apps = {}
    for list in cur_lists:
        apps[list["listid"]] = ro.lists.get_projects_from_list(connect_database(), list["listid"])
    return render_template("pages/curator/lists_dashboard.html", lists=cur_lists, projs=apps), 200

@curator.route("/lists/create")
def create_list():
    _verify_curator()
    all_apps = ro.projects.list_projects(connect_database())
    return render_template("pages/curator/wizard.html", projects=all_apps), 200

@curator.route("/lists/add", methods=["GET", "POST"])
def create_list_request():
    _verify_curator()
    all_projects_for_list = request.form.getlist("projects") if "projects" in request.form else None
    list_id = ro.lists.create_list(
        connect_database(), request.form["name"], request.form["blurb"], all_projects_for_list, session.get("cuid"))
    
    if not list_id:
        abort(500)
    return redirect(url_for('curator.lists_dashboard')), 200

@curator.route("/lists/<int:list_id>/manage")
def manage_list(list_id: int):
    edited_list = ro.lists.get_one_list(connect_database(), str(list_id))
    return render_template("pages/curator/list_manager.html", list=edited_list), 200

@curator.route("/lists/update", methods=["GET", "POST"])
def update_list_request():
    _verify_curator()
    try:
        ro.lists.update_list(connect_database(), request.form["id"], request.form["name"], request.form["blurb"])
        return redirect(url_for('curator.lists_dashboard'))
    except Exception as error:
        print(error)
        abort(500)

@curator.route("/lists/delete", methods=["GET", "POST"])
def delete_list_request():
    _verify_curator()
    try:
        ro.lists.delete_list(connect_database(), request.form["id"])
        return redirect(url_for('curator.lists_dashboard')), 200
    except Exception as error:
        print(error)
        abort(500)

@curator.route("/projects/<string:id>/inspect")
def inspect_project(id: str):
    _verify_curator()
    project = ro.projects.get_project(connect_database(), id)
    release = ro.releases.get_release(connect_database(), id)
    if not project or not release:
        abort(404)
    permissions = [] if not project["permissions"] else \
        [ro.projects.get_permission(connect_database(), val)
         for val in project["permissions"]]
    return render_template("pages/curator/inspect_manager.html", project=project, permissions=permissions, release = release)

@curator.route("/projects/<string:id>/approve", methods = ["GET","POST"])
def approve_release(id: str):
    _verify_curator()
    release = ro.releases.get_release(connect_database(), id)
    if (session.get("cuid") == release[0]["userid"]):
        ro.releases.approve_release(connect_database(), id)
        return redirect(url_for("curator.cur_dashboard")), 200
    else:
        abort(401)

@curator.route("/projects/reject", methods = ["GET","POST"])
def reject_release():
    _verify_curator()
    release = ro.releases.get_release(connect_database(), request.form["projectId"])
    if (session.get("cuid") == release[0]["userid"]):
        ro.releases.reject_release(connect_database(),release[0]["projectid"])
        return redirect(url_for("curator.cur_dashboard")), 200
    else:
        abort(401)