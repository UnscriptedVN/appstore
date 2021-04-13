--dummy database to debug with

delete from Account;
delete from UserAccount;
delete from Developer;
delete from Curator;
delete from Maintains;
delete from Project;
delete from Requires;
delete from Requires;
delete from Permission;
delete from Reviews;
delete from List;
delete from Includes;
delete from Release;
delete from DependsOn;
delete from License;


insert into License values ('3', 'This is some random license');
insert into Project values ('dev.unscriptedvn.candella.celeste-shell', '2', 'Celeste Shell','1.0.0','A desktop shell for Candella, inspired by Lomiri.', '3');
