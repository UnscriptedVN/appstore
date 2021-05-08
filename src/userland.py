# userland.py
# (C) 2021 Marquis Kurt, Nodar Sotkilava, and Unscripted VN Team.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https: //mozilla.org/MPL/2.0/.

from sys import stderr
from flask import Blueprint, render_template, abort, jsonify, request, session, url_for
from werkzeug.utils import redirect
from . import roland as ro
from .database import connect_database, frontpage_config

userland = Blueprint("userland", __name__,
                     template_folder="../templates", static_folder="../static")


@userland.route("/")
def index():
    # if not connect_database():
    #     return __database_failure()
    fconfig = frontpage_config()
    featured = ro.projects.get_project(
        connect_database(), fconfig["featured_project"])
    lists = [l for l in ro.lists.get_all_curator_lists(
        connect_database()) if l["name"] in fconfig["featured_lists"]]
    l_projects = {l["listid"]: ro.lists.get_projects_from_list(
        connect_database(), l["listid"]) for l in lists}
    return render_template("pages/index.html", featured=featured, lists=lists, l_projs=l_projects), 200


@userland.route("/apps/")
def prod_apps():
    try:
        all_apps = ro.projects.list_projects(connect_database(), filter_by_type=[
                                             ro.projects.ProjectType.App])
        error = None
    except Exception as err:
        all_apps = []
        error = err
        print(err, stderr)
    return render_template("pages/userland/apps.html", apps=all_apps, error=error), 200


@userland.route("/services/")
def services_list():
    try:
        all_apps = ro.projects.list_projects(connect_database(), filter_by_type=[
                                             ro.projects.ProjectType.CoreService])
        error = None
    except Exception as err:
        all_apps = []
        error = err
        print(err, stderr)
    return render_template("pages/userland/services.html", apps=all_apps, error=error), 200


@userland.route("/frameworks/")
def frameworks_list():
    try:
        all_apps = ro.projects.list_projects(connect_database(), filter_by_type=[
                                             ro.projects.ProjectType.Framework])
        error = None
    except Exception as err:
        all_apps = []
        error = err
        print(err, stderr)
    return render_template("pages/userland/frameworks.html", apps=all_apps, error=error), 200


@userland.route("/lists/")
def prod_lists():
    lists = ro.lists.get_all_curator_lists(connect_database())
    projects_for_lists = {}
    for list in lists:
        projects_for_lists[list["listid"]] = ro.lists.get_projects_from_list(
            connect_database(), list["listid"])
    return render_template("pages/lists.html", lists=lists, projects=projects_for_lists), 200


@userland.route("/search")
def prod_search():
    # FIXME: Implement this page.
    abort(500)


@userland.route("/apps/<string:project_id>/")
def project_detail(project_id):
    app = ro.projects.get_project(connect_database(), project_id)
    if not app:
        abort(404)
    reviews = ro.projects.get_reviews(connect_database(), project_id)
    reviewer_name = {}
    for review in reviews:
        reviewer_name[review["userid"]] = ro.accounts.get_account(connect_database(), review["userid"])["name"]
    permissions = [] if not app["permissions"] else \
        [ro.projects.get_permission(connect_database(), val)
         for val in app["permissions"]]

    developer = ro.projects.get_developer(connect_database(), app["id"])
    related = ro.projects.get_projects_by_developer(
        connect_database(), developer["userid"])

    return render_template(
        "pages/app_detail.html", app=app, permissions=permissions, dev=developer, rel=related, reviews = reviews, reviewer_name = reviewer_name), 200


@userland.route("/apps/developer/<int:developer_id>/")
def developer_detail(developer_id: int):
    developer = ro.accounts.get_account(connect_database(), developer_id)
    if not developer:
        abort(404)
    if developer["accounttype"] == ro.accounts.AccountType.UserAccount:
        abort(500)

    projects_by_dev = ro.projects.get_projects_by_developer(
        connect_database(), developer["userid"])
    return render_template("pages/dev_detail.html", developer=developer, projects=projects_by_dev), 200

@userland.route("/projects/add-review", methods=["GET", "POST"])
def add_project_review():
    ro.projects.post_review(connect_database(), session.get("cuid"), request.form["project_id"], request.form["rating"], request.form["comments"])
    return redirect(url_for("userland.project_detail", project_id = request.form['project_id']))

@userland.route("/lists/<int:id>/")
def list_detail(id: int):
    curated_list = ro.lists.get_one_list(connect_database(), str(id))
    projects = ro.lists.get_projects_from_list(connect_database(), str(id))
    curator = ro.accounts.get_account(
        connect_database(), curated_list["userid"])
    return render_template("pages/list_detail.html", list=curated_list, projects=projects, curator=curator), 200
