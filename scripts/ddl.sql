-- ddl.sql
-- (C) 2021 Marquis Kurt, Nodar Sotkilava, and Unscripted VN Team.

-- This Source Code Form is subject to the terms of the Mozilla Public
-- License, v. 2.0. If a copy of the MPL was not distributed with this
-- file, You can obtain one at https://mozilla.org/MPL/2.0/.

create table if not exists Account(
    userId serial primary key,
    githubId text,
    name text,
    accountType integer check (accountType > -1 and accountType < 3),
    email text unique check (email ~* '([a-z0-9_\.-]+)@([\da-z\.-]+)\.([a-z\.]{2,6})')
);

create table if not exists License(
    licenseId serial primary key,
    licenseName text
);

create table if not exists Project(
    projectId text primary key check (projectId similar to '[a-z]{2,}\.([a-z0-9]+(-[a-z0-9]+)*\.)+([a-z0-9\-]+)'),
    type integer,
    name text,
    version text,
    description text not null,
    blurb text,
    licenseId integer,
    projectIcon text,
    foreign key (licenseId) references License
);

create table if not exists Screenshot(
    screenId serial primary key,
    projectId text,
    screenUrl text,
    foreign key (projectId) references Project
);

-- TODO: Write a trigger to verify that a developer maintains this project,
-- not some user.
create table Maintains (
    projectId text,
    userId integer,
    primary key (projectId, userId),
    foreign key (projectId) references Project,
    foreign key (userId) references Account (userId) on delete set null
);

create table if not exists Permission(
    requiredKey text primary key,
    readableName text,
    description text
);

create table if not exists Requires(
    projectId text,
    requiredKey text,
    foreign key (projectId) references Project,
    foreign key (requiredKey) references Permission
);

create table if not exists Reviews(
    userId serial,
    projectId text,
    date timestamp with time zone,
    rating integer check (rating > 0 and rating < 6),
    comments text,
    foreign key (userId) references Account,
    foreign key (projectId) references Project
);

create table if not exists List(
    -- Add a trigger to make sure Curator is actually curating lists
    listId serial primary key,
    name text,
    blurb text,
    userId serial,
    foreign key (userId) references Account
);

create table if not exists Includes(
    listId serial,
    projectId text,
    foreign key (listId) references List,
    foreign key (projectId) references Project
);

create table Release (
    -- Add a trigger to make sure Curator approved this
    version text primary key,
    notes text,
    dowloadUrl text,
    projectId text,
    inspectDate timestamp with time zone,
    inspectStatus integer check (inspectStatus > -1 and inspectStatus < 3),
    userId serial,
    foreign key (projectId) references Project,
    foreign key (userid) references Account
);

create table if not exists DependsOn(
    dependentprojectId text,
    projectId text,
    primary key (dependentprojectId, projectId),
    foreign key (projectId) references Project,
    foreign key (dependentprojectId) references Project
);
