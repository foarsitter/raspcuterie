create table if not exists humidity
(
    id    integer primary key,
    time  text not null,
    value real not null
);

create table if not exists  temperature
(
    id    integer primary key,
    time  text not null,
    value real not null
);

create table if not exists  relay
(
    id      int
        constraint relay_pk
            primary key,
    time    text not null,
    value_1 INTEGER default 0,
    value_2 INTEGER default 0,
    value_3 INTEGER default 0,
    value_4 INTEGER default 0
);

create table if not exists  weight
(
    id    integer primary key,
    time  text not null,
    value real not null
);