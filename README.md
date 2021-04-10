# Candella Application Database (AppDB)
A database for the best and brightest Candella projects.

The **Candella Application Database (AppDB)** is an app store for projects written for the Candella operating framework. Users can download and leave reviews on projects, while developers can make releases available in a space that users can trust. Lists are curated by the Candella AppDB curation team, and all projects are reviewed under a small set of guidelines. 

## Build from source

**Requirements**

- PostgreSQL (on macOS, `brew install postgresql`; for Ubuntu/Debian, `apt install libpq-dev`)
- Pipenv
- Python 3.8 or greater

Ensure that you have the PostgreSQL dependencies installed before starting. Clone the repository and run `pipenv install` to install the dependencies needed to run the project.

## Setting up the app

You'll need to create an app on GitHub to support GitHub-based logins, as the database does not store passwords or have its own account system. Create an environment file called `.env` in the root of the project with the same fields as listed in `example.env`.

To run the application as-is, run `pipenv run dev`.

## License

The source code for the Candella AppDB is licensed under the Mozilla Public License, v2.0. If the license is not provided with the source code, you can obtain it at https://www.mozilla.org/en-US/MPL/2.0/.
