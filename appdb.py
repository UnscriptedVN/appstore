# appdb.py
# (C) 2021 Marquis Kurt, Nodar Sotkilava, and Unscripted VN Team.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from flask import Flask, render_template, json, session, request, jsonify
import psycopg2
import psycopg2.extras
import sys
import psycopg2.extensions

app = Flask(__name__)
app.config.from_pyfile("config.py")
app.config['DEBUG'] = True

#Establish connection to the DB
conn = None
cur = None
try:
        
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect( host = app.config['PSQL_HOST'], database = app.config['PSQL_DB'], 
                    user = app.config['PSQL_USER'], password = app.config['PSQL_PWD'])
        
        
        cur = conn.cursor()

        print('PostgreSQL database version:', file = sys.stderr)
        cur.execute("SELECT version()")

        db_version = cur.fetchone()
        
        print(db_version, file = sys.stderr)

        cur.close()
        
except(Exception, psycopg2.DatabaseError) as error:
    print(error, file = sys.stderr)

# TODO: Add routes here

#Returns 404 if something goes wrong
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

#Returns OK if connected
@app.route("/")
def connect():
    return "200", 200

#SELECT all the projects from Project
@app.route("/api/v1/projects/all", methods = ['GET'])
def get_projects():
    cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    cur.execute('SELECT * FROM Project')
    all_projects = cur.fetchall()
    cur.close()
    return(jsonify(all_projects))

#SELECTs a specific project based on the parameters passed
@app.route("/api/v1/projects", methods = ['GET'])
def get_project():
    query_parameters = request.args

    projectId = query_parameters.get('projectId')
    type = query_parameters.get('type')
    name = query_parameters.get('name')
    version = query_parameters.get('version')
    description = query_parameters.get('description')
    licenseId = query_parameters.get('licenseId')

    query = 'SELECT * FROM Project WHERE'
    to_filter = []

    #This is fucky wucky rewrite
    if projectId:
        query+= ' projectId=%s AND'
        to_filter.append(psycopg2.extensions.adapt(projectId))
    if type:
        query+= ' type=%s AND'
        to_filter.append(type)
    if name:
        query+= ' name=%s AND'
        to_filter.append(name)
    if version:
        query+= ' version=%s AND'
        to_filter.append(version)
    if description:
        query+= ' description=%s AND'
        to_filter.append(description)
    if licenseId:
        query+= ' licenseId=%s AND'
        to_filter.append(licenseId)
    if not(projectId or type or name or version or description or licenseId):
        return page_not_found(404)
    query = query[:-4]

    cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)

    cur.execute(query, to_filter)

    results = cur.fetchall()

    cur.close()

    return (jsonify(results))

if __name__ != "__main__":
    application = app