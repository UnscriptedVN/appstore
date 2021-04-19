--dummy database to debug with

delete from Account;
delete from Maintains;
delete from Project;
delete from Screenshot;
delete from Requires;
delete from Requires;
delete from Permission;
delete from Reviews;
delete from List;
delete from Includes;
delete from Release;
delete from DependsOn;
delete from License;


insert into License values (1, 'This is some random license');
insert into Project values (
    'dev.unscriptedvn.candella.celeste-shell',
    '2',
    'Celeste Shell',
    '1.0.0',
    'A desktop shell for Candella, inspired by Lomiri.',
    null,
    1,
    'https://github.com/UnscriptedVN/candella/raw/root/game/System/CoreServices/Celeste.aoscservice/Resources/Iconset/512.png'
);

insert into Screenshot (projectId, screenUrl) values ('dev.unscriptedvn.candella.celeste-shell', 'https://candella.unscriptedvn.dev/images/celeste/drawer.png');
