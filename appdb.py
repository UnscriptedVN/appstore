# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from flask import Flask, render_template, json, session, request, jsonify

app = Flask(__name__)
app.config.from_pyfile("config.py")

# TODO: Add routes here

if __name__ != "__main__":
    application = app