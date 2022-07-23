-- db_name = flask

-- public.users definition

-- Drop table

-- DROP TABLE public.users;

CREATE TABLE public.users (
	id serial4 NOT NULL,
	"name" varchar(25) NOT NULL,
	CONSTRAINT users_pkey PRIMARY KEY (id)
);


-- public.advs definition

-- Drop table

-- DROP TABLE public.advs;

CREATE TABLE public.advs (
	id serial4 NOT NULL,
	title varchar(25) NOT NULL,
	description text NOT NULL,
	created_at timestamp NULL DEFAULT CURRENT_TIMESTAMP,
	user_id int4 NULL,
	CONSTRAINT advs_pkey PRIMARY KEY (id)
);


-- public.advs foreign keys

ALTER TABLE public.advs ADD CONSTRAINT advs_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;

INSERT INTO users (name)VALUES('Коля'),('Валя'),('Юля');