-- defaults.sql
-- (C) 2021 Marquis Kurt, Nodar Sotkilava, and Unscripted VN Team.

-- This Source Code Form is subject to the terms of the Mozilla Public
-- License, v. 2.0. If a copy of the MPL was not distributed with this
-- file, You can obtain one at https://mozilla.org/MPL/2.0/.

-- Load the default permission set from Candella documentation.
delete from Permission;

insert into Permission values ('file_system', 'File system access', 'Includes access to the Candella file system');
insert into Permission values ('notifications', 'Send notifications', 'Sends alerts, banners, and/or sound notifications');
insert into Permission values ('system_events', 'Manage system events', 'Listens and responds to system events');
insert into Permission values ('manage_users', 'Manage user accounts', 'Utilizes account service to manage multiple users');
insert into Permission values ('virtual_platform', 'Access MeteorVM', 'Utilizes the MeteorVM platform to execute instructions');