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
