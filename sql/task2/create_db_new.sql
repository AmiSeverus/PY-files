create table if not exists Genders(
id serial primary key,
name varchar(16) not null unique
);

create table if not exists Singers(
id serial primary key,
name varchar(16) not null unique
);

create table if not exists SingersGenders(
singer_id integer references Singers(id),
gender_id integer references Genders(id),
constraint pk_sg primary key (singer_id, gender_id)
);

create table if not exists Albums(
id serial primary key,
name varchar(16) not null,
year integer not null check(year > 0)
);

create table if not exists SingersAlbums(
singer_id integer references Singers(id),
album_id integer references Albums(id),
constraint pk_sa primary key (singer_id, album_id)
);

create table if not exists Songs(
id serial primary key,
album_id integer references Albums(id),
name varchar(16) not null,
length integer not null
);


create table if not exists Collections(
id serial primary key,
name varchar(16) not null,
year integer not null check(year > 0)
);

create table if not exists CollectionsSongs(
collection_id integer references Collections(id),
song_id integer references Songs(id),
constraint pk_cs primary key (collection_id, song_id)
);




