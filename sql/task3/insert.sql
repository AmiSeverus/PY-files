insert into Singers (name)VALUES('John Smith'),
								('Sarah Jessica-Parker'),
								('Adele'),
								('Will Smith'),
								('Marissa'),
								('Bon Jovi'),
								('Lev Leshchenko'),
								('Jamiroquai');
insert into Genders(name)VALUES('pop'),
							   ('rock'),
							   ('classic'),
							   ('hip-hop'),
							   ('electro');
insert into SingersGenders(singer_id, gender_id)VALUES(1,4),
													  (2,1),
													  (3,1),
													  (3,3),
													  (4,4),
													  (5,1),
													  (5,2),
													  (6,3),
													  (7,5);

insert into Albums (name,year)VALUES('Man in Black', 2017),
									('Electro', 2016),
									('Back to USSR', 2018),
									('Adele', 2019),
									('Rossia', 2020),
									('Sex in the Sity', 2021),
									('Wild wild west', 2018),
									('Calling', 2019);
insert into SingersAlbums(singer_id,album_id)VALUES(4,1),
												   (5,1),
												   (8,2),
												   (6,3),
												   (3,4),
												   (7,5),
												   (2,6),
												   (5,6),
												   (5,7),
												   (3,8);

insert into Songs(album_id,name,length)VALUES(1,'Man in Black 1', 200),
											 (1, 'Man in Black 2', 300),
											 (2, 'Electro music', 290),
											 (3, 'USSR', 180),
											 (3, 'Russia', 250),
											 (3, 'My Moscow', 135),
											 (4, 'Sorry', 357),
											 (4, 'Believe', 263),
											 (5, 'Vechera', 198),
											 (5, 'Berezka', 320),
											 (6, 'Sex in the City 1', 390),
											 (6, 'Sex in the City 2', 450),
											 (7, 'WWW', 285),
											 (8, 'Calling', 340),
											 (8, 'Hello', 310);

insert into Collections(name, year)VALUES('Russia', 2018),
										 ('Women', 2021),
										 ('Men', 2017),
										 ('Films', 2019),
										 ('Electro', 2016),
										 ('Hip-hop', 2019),
										 ('Classic', 2020),
										 ('Pop', 2019),
										 ('Rock', 2017);
										
insert into CollectionsSongs (collection_id, song_id)VALUES(6,1),
														   (4,1),
														   (6,2),
														   (4,2),
														   (3,3),
														   (5,3),
														   (1,4),
														   (9,4),
														   (1,5),
														   (9,5),
														   (1,6),
														   (9,6),
														   (2,7),
														   (2,8),
														   (1,9),
														   (7,9),
														   (7,10),
														   (1,10),
														   (8,11),
														   (4,11),
														   (8,12),
														   (4,12),
														   (4,13),
														   (3,13),
														   (6,13),
														   (2,14),
														   (2,15);

							   