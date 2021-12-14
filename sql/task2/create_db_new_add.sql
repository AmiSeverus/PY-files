create table if not exists Employees(
id serial primary key,
name varchar(16) not null,
div_name varchar(16) not null,
manager_id integer references Employees(id)
);