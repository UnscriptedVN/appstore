# authentication.py
# (C) 2021 Marquis Kurt, Nodar Sotkilava, and Unscripted VN Team.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https: //mozilla.org/MPL/2.0/.

from flask import Blueprint, render_template, request, redirect, abort, session, url_for, current_app
from .database import connect_database
from . import roland as ro

auth = Blueprint("auth", __name__, template_folder="../templates", static_folder="../static", url_prefix="/auth")


@auth.route("/register")
def auth_register():
    # if not connect_database():
    #     return __database_failure()
    if not session.get("rxw_reg"):
        abort(401)
    new_account = ro.accounts.get_account(connect_database(), session["cuid"])
    session.modified = True
    return render_template("pages/acct_register.html", account=new_account), 200


@auth.route("/register/callback", methods=["GET", "POST"])
def update_account_type():
    if not session.get("rxw_reg") or not session.get("login_token"):
        abort(401)
    account_type = ro.accounts.AccountType(int(request.form["account_type"]))
    ro.accounts.update_account_type(
        connect_database(), session.get("cuid"), account_type=account_type)
    del session["rxw_reg"]
    return redirect(url_for("userland.index"))


@auth.route("/login")
def auth_login():
    # if not connect_database():
    #     return __database_failure()
    if session.get("cuid") or session.get("login_token"):
        return redirect(url_for("auth_register")) if session["rxw_reg"] else redirect(url_for("index"))
    client_id = current_app.config['GH_CLIENT_ID']
    auth_url = f"https://github.com/login/oauth/authorize?client_id={client_id}"\
        + "&scope=user:email%20read:user&allow_signup=true"
    return render_template("pages/login.html", gh_auth_url=auth_url), 200


@auth.route("/logout")
def auth_logout():
    if session.get("cuid"):
        del session["cuid"]
    if session.get("login_token"):
        del session["login_token"]
    session.modified = True
    return redirect(url_for("userland.index"))
