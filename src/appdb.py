# appdb.py
# (C) 2021 Marquis Kurt, Nodar Sotkilava, and Unscripted VN Team.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from flask import Flask, render_template, session, url_for
from .api import api as api_blueprint
from .userland import userland as userland_blueprint
from .developer import developer as developer_blueprint
from .authentication import auth as auth_blueprint
from .curator import curator as curator_blueprint
from .database import *
import sys

app = Flask(__name__, template_folder="../templates", static_folder="../static")
app.config.from_pyfile("config.py")
app.config['DEBUG'] = True


with app.app_context():
    app.register_blueprint(api_blueprint)
    app.register_blueprint(userland_blueprint)
    app.register_blueprint(developer_blueprint)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(curator_blueprint)

@app.before_request
def register_session():
    session.permanent = True

@app.after_request
def after_request(response):
    close_database()
    return response

def database_failure():
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

@app.errorhandler(400)
def err_internal_server(e):
    return render_template("pages/error.html", errcode=400), 400


if not app.config['DEBUG']:
    @app.errorhandler(Exception)
    def internal_server_error(e):
        print(e, file=sys.stderr)
        return render_template("pages/error.html", errcode=500), 500

if __name__ != "__main__":
    application = app
