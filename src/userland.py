# userland.py
# (C) 2021 Marquis Kurt, Nodar Sotkilava, and Unscripted VN Team.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https: //mozilla.org/MPL/2.0/.

from os import path, listdir
from sys import stderr
from flask import Blueprint, render_template, abort, jsonify, request, session, url_for, Markup, redirect, current_app
from commonmark import commonmark
from . import roland as ro
from .database import connect_database, frontpage_config

userland = Blueprint("userland", __name__,
                     template_folder="../templates", static_folder="../static")


def _retrieve_docs_list():
    """Returns a dictionary containing the Markdown files in the pages directory.

    The keys correspond to the filenames, excluding the extension, and the values correspond to their HTML title
        versions.
    """
    return {
        file.replace(".md", ""): file.replace(".md", "").replace("_", " ").title() \
        for file in listdir("pages") if not file.startswith(".")
    }


@userland.route("/")
def index():
    """Renders the custom homepage as provided by the administrator.
    
    For environments where providing a json file is not feasible, admins can supply FRONTPAGE_CONFIG to hange 
        customization.
    """
    # if not connect_database():
    #     return __database_failure()
    fconfig = frontpage_config()
    featured = ro.projects.get_project(
        connect_database(), fconfig["featured_project"]) if "featured_project" in fconfig else None
    lists = [l for l in ro.lists.get_all_curator_lists(
        connect_database()) if l["name"] in fconfig["featured_lists"]] if "featured_lists" in fconfig else []
    l_projects = {l["listid"]: ro.lists.get_projects_from_list(
        connect_database(), l["listid"]) for l in lists}
    return render_template("pages/index.html", featured=featured, lists=lists, l_projs=l_projects), 200


@userland.route("/docs/<string:page_name>/")
def documentation(page_name: str):
    """Support for documentation pages provided in Markdown are rendered safely according to Commonmark specification."""

    if not path.isfile(f"pages/{page_name}.md"):
        abort(404)
    with open(f"pages/{page_name}.md", 'r') as pagefile:
        content = Markup(commonmark(pagefile.read()))

    docs = _retrieve_docs_list()
    title = page_name.replace("_", " ").title()
    return render_template("markdown.html", content=content, title=title, docs=docs), 200


@userland.route("/apps/")
def prod_apps():
    """Renders a page of all the projects that are type App"""

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
    """Renders a page of all the projects that are type Services"""

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
    """Renders a page of all the projects that are type Framework"""

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
    """Renders the curated lists provided by Curators to the User"""

    lists = ro.lists.get_all_curator_lists(connect_database())
    projects_for_lists = {}
    for list in lists:
        projects_for_lists[list["listid"]] = ro.lists.get_projects_from_list(
            connect_database(), list["listid"])
    return render_template("pages/lists.html", lists=lists, projects=projects_for_lists), 200


@userland.route("/apps/<string:project_id>/")
def project_detail(project_id):
    """Renders a detailed page of project with a given project_id.
    
        Page includes download link, summary of the project, user reviews, and permisions.
    """

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
        "pages/app_detail.html", app=app, permissions=permissions, dev=developer, rel=related, reviews = reviews,
        reviewer_name = reviewer_name), 200


@userland.route("/apps/developer/<int:developer_id>/")
def developer_detail(developer_id: int):
    """Renders a page of all the projects made by the specified developer."""

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
    """API endpoint to add a user review to the project.
    
        Users are then redirected to the project page.
    """

    ro.projects.post_review(connect_database(), session.get("cuid"), request.form["project_id"], request.form["rating"],
    request.form["comments"])
    return redirect(url_for("userland.project_detail", project_id = request.form['project_id']))

@userland.route("/lists/<int:id>/")
def list_detail(id: int):
    """Renders a detailed view of the curated list, including all the projects in it"""

    curated_list = ro.lists.get_one_list(connect_database(), str(id))
    projects = ro.lists.get_projects_from_list(connect_database(), str(id))
    curator = ro.accounts.get_account(
        connect_database(), curated_list["userid"])
    return render_template("pages/list_detail.html", list=curated_list, projects=projects, curator=curator), 200

@userland.route("/account/settings")
def account_settings():
    """Renders a page for Users to manage their account.
    
        Users are able to change their name and email, manage GitHub Data and delete their account
    """

    if not session.get("cuid") or not session.get("login_token"):
        abort(401)
    user = ro.accounts.get_account(connect_database(), int(session.get("cuid")))
    rxw_cid = current_app.config["GH_CLIENT_ID"]
    return render_template("pages/userland/account.html", user=user, rxw_cid=rxw_cid), 200


@userland.route("/account/update", methods=["GET", "POST"])
def update_account():
    """API endpoint that updates the User's name and/or email in the DB."""

    if "userId" not in request.form:
        abort(400)
    if str(session.get("cuid")) != str(request.form["userId"]):
        abort(403)
    try:
        ro.accounts.update_user_settings(
            connect_database(), request.form["userId"], request.form["email"], request.form["name"])
        return redirect(url_for('userland.account_settings'))
    except Exception as error:
        print(error, stderr)
        abort(500)

@userland.route("/account/delete", methods=["GET", "POST"])
def yeetus_deeletus_user():
    """As the function name implies, API endpoint that deletes that User's account."""
    
    if "userId" not in request.form or "rxw_delete_confirm" not in request.form:
        abort(400)
    if request.form["rxw_delete_confirm"] != "I understand. Delete my account.":
        abort(400, description='User did not confirm account deletion.')
    if str(session.get("cuid")) != str(request.form["userId"]):
        abort(403)
    try:
        ro.accounts.delete_user(
            connect_database(), request.form["userId"], ro.accounts.AccountType(int(request.form["type"])))
        return redirect(url_for('auth.auth_logout'))
    except Exception as error:
        print(error, stderr)
        abort(500)
