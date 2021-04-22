# appdb.py
# (C) 2021 Marquis Kurt, Nodar Sotkilava, and Unscripted VN Team.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from flask import Flask, render_template, jsonify, request, redirect, abort, session, g as gblspace
from flask.helpers import url_for
from . import roland as ro
from .api import api as api_blueprint
from .userland import userland as userland_blueprint
from .database import *
import sys

app = Flask(__name__, template_folder="../templates", static_folder="../static")
app.config.from_pyfile("config.py")
app.config['DEBUG'] = True

with app.app_context():
    app.register_blueprint(api_blueprint)
    app.register_blueprint(userland_blueprint)

@app.after_request
def after_request(response):
    close_database()
    return response

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
# MARK: AUTHENTICATION PAGES              #
###########################################

@app.route("/auth/register")
def auth_register():
    if not connect_database():
        return __database_failure()
    if not session.get("rxw_reg"):
        abort(401)
    new_account = ro.accounts.get_account(connect_database(), session["cuid"])
    session.modified = True
    return render_template("pages/acct_register.html", account=new_account), 200


@app.route("/auth/register/callback", methods=["GET", "POST"])
def update_account_type():
    if not session.get("rxw_reg") or not session.get("login_token"):
        abort(401)
    account_type = ro.accounts.AccountType(int(request.form["account_type"]))
    ro.accounts.update_account_type(connect_database(), session.get("cuid"), account_type=account_type)
    del session["rxw_reg"]
    return redirect(url_for("index"))

@app.route("/auth/login")
def auth_login():
    if not connect_database():
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
    return redirect(url_for("userland.index"))

###########################################
# MARK: DEVELOPER PAGES                   #
###########################################


@app.route("/developer/dashboard")
def dev_dashboard():
    acct = ro.accounts.get_account(connect_database(), session.get("cuid"))
    if not acct or acct["accounttype"] != ro.accounts.AccountType.Developer:
        abort(401)
    return "200", 200

###########################################
# MARK: CURATOR PAGES                     #
###########################################


@app.route("/curator/dashboard")
def cur_dashboard():
    acct = ro.accounts.get_account(connect_database(), session.get("cuid"))
    if not acct or acct["accounttype"] != ro.accounts.AccountType.Curator:
        abort(401)
    return "200", 200


if __name__ != "__main__":
    application = app
