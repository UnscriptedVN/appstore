# api.py
# (C) 2021 Marquis Kurt, Nodar Sotkilava, and Unscripted VN Team.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https: //mozilla.org/MPL/2.0/.

import sys
from flask import Blueprint, jsonify, request, redirect, abort, url_for, current_app
from . import roland as ro
from .database import connect_database

api = Blueprint("api", __name__, template_folder="../templates", static_folder="../static", url_prefix="/api/v1")

@api.route("/authenticate", methods=["GET"])
def authenticate():
    query = request.args
    if query.get("error") or not query.get("code"):
        return jsonify({
            "error": "GitHub authorization failed."
        }), 400
    try:
        redirect_to = ro.auth.authenticate_with_github(
            query.get("code"),
            client_id=current_app.config["GH_CLIENT_ID"],
            client_secret=current_app.config["GH_CLIENT_SECRET"],
            app_database=connect_database())
        return redirect(url_for("auth.auth_register")) if redirect_to == "registered" \
            else redirect(url_for("userland.index"))
    except Exception as error:
        print(error, file=sys.stderr)
        abort(500)


@api.route("/projects/<string:id>", methods=["GET"])
def api_single_project(id: str):
    project = ro.projects.get_project(connect_database(), id)
    if not project:
        return jsonify({"error": "Record not found"}), 404
    return jsonify(project)


@api.route("/projects/<string:id>/releases", methods=['GET'])
def api_project_releases(id: str):
    project = ro.projects.get_project(connect_database(), id)
    if not project:
        return jsonify({"error": "Record not found"}), 404

    releases = ro.projects.get_releases(connect_database(), id)
    return jsonify(releases)


@api.route("/projects", methods=['GET'])
def api_get_project():
    return jsonify(ro.projects.list_projects(connect_database()))


@api.route("/search", methods=["GET"])
def api_search():
    return ro.search.search(connect_database())


@api.route("/users/<int:id>", methods=['GET'])
def api_get_user(id: int):
   account = ro.accounts.get_account(connect_database(), id)
   if not account:
       return jsonify({"error": "Record not found"}), 404
   return jsonify(account)


@api.route("/lists", methods=["GET"])
def api_get_all_lists():
    return jsonify(ro.lists.get_all_curator_lists(connect_database()))


@api.route("/lists/<string:id>", methods=['GET'])
def api_single_list(id: str):
    return jsonify(ro.lists.get_one_list(connect_database(), id))


@api.route("/lists/curator/<string:id>", methods=['GET'])
def api_curator_lists(id: str):
    return jsonify(ro.lists.get_curator_lists(connect_database(), id))


@api.route("/lists/project/<string:id>", methods=['GET'])
def api_get_project_in_curator_list(id: str):
    return jsonify(ro.lists.get_project_in_curator_list(connect_database(), id))
