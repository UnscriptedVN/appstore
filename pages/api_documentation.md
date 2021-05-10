# API Documentation

The Candella AppDB includes a basic API that lets developers fetch data from the AppDB and incorporate it into their own apps, websites, or services.

> Warning: Please note that the API during the Open Beta is pre-release and some endpoints may change over time.

## GET `/api/v1/projects`

Returns a list of the `Project` entities available on the AppDB.

## GET `/api/v1/projects/:id`

Returns the data for a project with a given ID.

**Parameters**

- `id` (str): The project's bundle identifier

**Returns**

- A `Project` entity with the associated data for the project.

**Raises**

- `404`: No projects with the specified ID were found.

**Example**

```json
{
  "blurb": " Celeste Shell (formerly Caberto Shell) is a Lomiri/Unity8-inspired desktop shell for Candella. Find and launch your favorite apps with ease. Customize Celeste to your liking with custom settings per-user.", 
  "description": "A desktop shell for the rest of us", 
  "developer": 1, 
  "icon": "https://raw.githubusercontent.com/UnscriptedVN/candella/root/game/System/CoreServices/Celeste.aoscservice/Resources/Iconset/512.png", 
  "id": "dev.unscriptedvn.candella.celeste-shell", 
  "latest_version": null, 
  "license": "MPL-2.0", 
  "name": "Celeste Shell", 
  "permissions": [
    "file_system", 
    "manage_users"
  ], 
  "releases": [], 
  "screenshots": [
    "https://candella.unscriptedvn.dev/img/desktop.png", 
    "https://candella.unscriptedvn.dev/images/celeste/drawer.png"
  ], 
  "type": "core service"
}
```

## GET `/api/v1/projects/:id/releases`

Returns a list of `Release` entities associated with a project.

**Parameters**

- `id` (str): The project's bundle identifier

**Returns**

- A list of `Release` entities.

**Raises**

- `404`: The project with the specified ID doesn't exist.

**Example**

```json
[
  {
    "download": "https://github.com/UnscriptedVN/candella/releases/tag/v21.04-beta3", 
    "notes": "The following release is the third prerelease in the v21.x series and is subject to change. This prerelease is merely a minor beta release, as it now builds against the Ren'Py 7.4.4 SDK.", 
    "release_date": "Mon, 10 May 2021 23:13:21 GMT", 
    "version": "21.04-beta3"
  }
]
```

## GET `/api/v1/lists`

Returns a list of `List` entities on the AppDB.

## GET `/api/v1/lists/:id`

Returns a `List` entity with a list given its ID.

**Parameters**

- `id` (str): The list's identifier

**Returns**

- A `List` entity representing the recommended list.

**Raises**

- `404`: The list with the specified ID doesn't exist.

**Example**

```json
{
  "blurb": "Candella comes bundled with several core services and apps that make the essential experience. Check them out here!", 
  "listid": 1, 
  "name": "Bundled with Candella", 
  "userid": 1
}
```


## `Project` entity

An entity that represents an app, core service, or framework.

**Attributes**

- `blurb` (str, Optional): A longer description about the service.
- `description` (str): A short summary of the project.
- `developer` (id): The developer ID associated with the project.
- `icon` (str): A URL pointing to the project's icon.
- `id` (str): The bundle identifier of the project.
- `latest_version` (str, Optional): The latest version number string.
- `license` (str): An SPDX expression representing the project's license.
- `name` (str): The name of the project.
- `permissions` (list): The list of permissions the project needs in Candella.
- `releases` (list): A list of `Release` entities for this project.
- `screenshots` (list): A list of URLs that point to project screenshots.
- `type` (str): The type of project: either an `app`, `core service`, or `framework`.

## `Release` entity

An entity that represents a release.

**Attributes**

- `download` (str): The URL to download the version of the release.
- `notes` (str): The release notes or changelog for this release.
- `release_date` (str): The date string of when the release was approved.
- `version` (str): The version associated with this release.

## `List` entity

An entity that represents a curated list.

**Attributes**

- `blurb` (str): The description/blurb of this list.
- `listid` (int): The ID of the list in the DB.
- `name` (str): The name of the list.
- `userid` (int): The curator ID associated with the curator that maintains the list.