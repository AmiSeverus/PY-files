create table Singers(
id serial primary key,
name varchar(16) not null unique
);

create table Albums(
id serial primary key,
singer_id integer references Singers(id),
name varchar(16) not null,
year integer not null check(year > 0)
);

create table Songs(
id serial primary key,
album_id integer references Albums(id),
name varchar(16) not null,
length varchar(8) not null
);


