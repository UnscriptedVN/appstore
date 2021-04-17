create table Account (
    userId serial primary key,
    githubId text,
    name text,
    accountType integer check (accountType > -1 and accountType < 3),
    email unique text check (email ~* '([a-z0-9_\.-]+)@([\da-z\.-]+)\.([a-z\.]{2,6})')
);

create table License(
    licenseId serial primary key,
    licenseName text
);

create table Project(
    projectId text primary key check (projectId similar to '[a-z]{2,}\.([a-z0-9]+(-[a-z0-9]+)*\.)+([a-z0-9\-]+)'),
    type integer,
    name text,
    version text,
    description text,
    licenseId serial,
    foreign key (licenseId) references License
);

create table Maintains (
    projectId text,
    githubId text,
    primary key (projectId, githubId),
    foreign key (projectId) references Project,
    foreign key (githubId) references Account(githubId) on delete set null
);

create table Permission(
    requiredKey text primary key,
    readableName text,
    description text
);

create table Requires(
    projectId text,
    requiredKey text,
    foreign key (projectId) references Project,
    foreign key (requiredKey) references Permission
);

create table Reviews(
    userId serial,
    projectId text,
    date timestamp with time zone,
    rating integer check (rating > 0 and rating < 6),
    comments text,
    foreign key (userId) references Account,
    foreign key (projectId) references Project
);

create table List(
    -- Add a trigger to make sure Curator is actually curating lists
    listId serial primary key,
    name text,
    blurb text,
    userId serial,
    foreign key (userId) references Account
);

create table Includes(
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

create table DependsOn(
    dependentprojectId text,
    projectId text,
    primary key (dependentprojectId, projectId),
    foreign key (projectId) references Project,
    foreign key (dependentprojectId) references Project
);
