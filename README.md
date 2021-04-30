# Candella Application Database (AppDB)

A database for the best and brightest Candella projects.

The **Candella Application Database (AppDB)** is an app store for projects written for the Candella operating framework. Users can download and leave reviews on projects, while developers can make releases available in a space that users can trust. Lists are curated by the Candella AppDB curation team, and all projects are reviewed under a small set of guidelines.

## Build from source

**Requirements**

- PostgreSQL (on macOS, `brew install postgresql`; for Ubuntu/Debian, `apt install postgres-12`)
- Pipenv
- Python 3.8 or greater
- (Optional, but recommended) Docker and Docker Compose

### Setting up the app via Docker

The Candella AppDB can be easily deployed to any server via Docker. Ensure that you have Docker and Docker Desktop installed before setting up AppDB with Docker.

Clone the repository from GitHub, then run `docker-compose build` to build the Docker image for the Candella frontend. This will also pull the PostgreSQL image from Docker.

Set up the database and run the AppDB containers by running `docker-compose up -d`.

### Setting up the app manually

Ensure that you have the PostgreSQL dependencies installed before starting. Clone the repository and run `pipenv install` to install the dependencies needed to run the project.

You'll need to create an app on GitHub to support GitHub-based logins, as the database does not store passwords or have its own account system. Create an environment file called `.env` in the root of the project with the same fields as listed in `example.env`.

Before running the app, open the `psql` client in the database specified in your `.env` file. Run the script files in the scripts directory in this order:

- `ddl.sql` (This creates the schemas needed)
- `defaults.sql` (This imports default values for some fields)
- `spdxImport.sql` (This imports all of the valid SPDX expressions for the license field.)

> :information: In the future, this may be replaced with a Python setup script.

To run the application as-is, run `pipenv run dev`.

### Create the administrator account

You'll need to authenticated with the database by heading to the path `/auth/login` at the URL for the AppDB in your browser.

This will create the first account in the database. To access the developer and curator dashboards, run the following commands in `psql`:

```sql
select id from Account; -- This will fetch your user ID.
update Account set accountType = 2 where userId = -1; -- Replace -1 with your user ID from the prev. command.
```

> Note: If you ran setup with Docker, you'll need to launch a shell inthe database container to access psql. Additionally, you'll need to supply the following arguments: `-U docker -d appdb__docker`.

### Configure the homepage

To configure the featured project and the lists that appear on the homepage, you'll want to create a `frontpage.json` file and specify the `featured_project` and `featured_lists` fields. You can take a look at `example.frontpage.json` to look at an example.

> :warning: You need to make sure that these projects and lists specified in the JSON file exist in the database beforehand.

## License

The source code for the Candella AppDB is licensed under the Mozilla Public License, v2.0. If the license is not provided with the source code, you can obtain it at https://www.mozilla.org/en-US/MPL/2.0/.
