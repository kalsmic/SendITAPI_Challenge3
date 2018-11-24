drop table if exists parcels;
drop table if exists users;
create table if not exists users
(
  user_id   serial not null
    constraint users_pkey
    primary key,
  username  varchar(25),
  firstname varchar(25),
  lastname  varchar(25),
  password  varchar(255),
  email     varchar(150),
  is_admin  BOOLEAN DEFAULT FALSE
);

alter table users
  owner to postgres;


create table if not exists parcels
(
  parcel_id           serial       not null primary key,
  item                varchar(150),
  source_address      varchar(150),
  destination_address varchar(150),
  present_location    varchar(150) NOT NULL,
  status              varchar(10) default 'pending',
  owner_id            integer
    constraint parcels_owner_id_fkey
    references users
    on update cascade on delete cascade
);

alter table parcels
  owner to postgres;
INSERT INTO users ( username, firstname, lastname, password, email, is_admin)
VALUES ('admin',
        'admin',
        'admin',
        'sha256$Rzrg0Xgr$2a090c34bf0a07e9f1ce19559a62464048268fff0aa3ce59599bf71cfc469a25',
        'admin@sendit.com',
        true);
INSERT INTO users ( username, firstname, lastname, password, email, is_admin)
VALUES ('user1',
        'user1',
        'user1',
        'sha256$qVpAKAqO$7465343021019bf1e015cf60c5f36bf5ca232b6fcd5d7c7ab5f2d8c6a8388984',
        'user1@sendit.com',
        false);
INSERT INTO users ( username, firstname, lastname, password, email, is_admin)
VALUES ('user2',
        'user2',
        'user2',
        'sha256$ZNLbN6ws$767a1cce1c344620d09ff92d1cb82ac2d9e331df27f7eaf5f00e6c77595a7682',
        'user2@sendit.com',
        false);
INSERT INTO parcels (parcel_id, item, source_address, destination_address, status, owner_id, present_location)
VALUES (1, 'HMIS Forms', 'Kotido', 'hoima', 'pending', 2, 'Hoima');
INSERT INTO parcels (parcel_id, item, source_address, destination_address, status, owner_id, present_location)
VALUES (2, 'laptop', 'Lira', 'Kampala', 'in transit', 2, 'Kamdin');
INSERT INTO parcels (parcel_id, item, source_address, destination_address, status, owner_id, present_location)
VALUES (3, 'Text Books', 'Mukono', 'Kololo', 'delivered', 2, 'Kololo');
INSERT INTO parcels (parcel_id, item, source_address, destination_address, status, owner_id, present_location)
VALUES (4, 'Text Books', 'Naalya', 'Ntinda', 'cancelled', 3, 'Naalya');