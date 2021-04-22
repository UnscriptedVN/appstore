# utils.py
# (C) 2021 Marquis Kurt, Nodar Sotkilava, and Unscripted VN Team.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import psycopg2 as psql

class DatabaseContext():
    """A clean and elegant solution for using database cursors like a file.

    When initializing this class with a context manager, the keyword arguments passed to this
        class will be passed down to the cursor when generated. The cursor will automatically
        close when exiting the context manager.

    Example:
        with DatabaseContext(db, cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            cursor.execute("select * from projects where projectId like 'dev.%'")
            results = cursor.fetchall()
    
    Arguments:
        - database: The database from where the cursor will come from.
        - **kwargs: Abritrary keyword arguments for the database cursor.
    """
    def __init__(self, database, **kwargs):
        self.database = database
        self.cursor_args = kwargs

    def __enter__(self):
        self.cursor = self.database.cursor(**self.cursor_args)
        return self.cursor
    
    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.cursor.close()


def load_database(with_app_config: dict):
    """Connect to the database that hosts the AppDB database information.

    Arguments:
        - with_app_config (dict): The Flask app configuration that contains the information needed
            to connect to the database.

    Returns:
        The connected database.
    """
    database = psql.connect(host=with_app_config['PSQL_HOST'], database=with_app_config['PSQL_DB'],
                            user=with_app_config['PSQL_USER'], password=with_app_config['PSQL_PWD'])

    if with_app_config['DEBUG']:
        with DatabaseContext(database) as ctx:
            ctx.execute("SELECT version()")
            print(f"PSQL Version: {ctx.fetchone()}")
    
    return database