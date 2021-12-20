select name, year from albums where year = 2018;

select name, length from songs where length = (select max(length) from songs);

select name from songs where length >= 3.5*60;

select name from collections where year between 2018 and 2020;

select name from singers where name not like '%_ _%';

select name from songs where name ilike '%my%' or name ilike '%мой%'; 