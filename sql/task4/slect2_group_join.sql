SELECT gender_id, COUNT(singer_id) FROM singersgenders
GROUP BY gender_id;

SELECT album_id, COUNT(id) AS songs_cnt FROM songs
GROUP BY album_id
HAVING album_id IN (SELECT id FROM albums WHERE YEAR BETWEEN 2019 AND 2020);

SELECT album_id, AVG(LENGTH) FROM songs
GROUP BY album_id;

SELECT * FROM singers
WHERE id NOT IN (
	SELECT singer_id FROM singersalbums WHERE album_id IN (
		SELECT id FROM albums WHERE YEAR = 2020))
ORDER BY id;

SELECT c.name FROM collections AS c
JOIN collectionssongs AS cs
ON c.id = cs.collection_id 
WHERE cs.song_id IN (
	SELECT id FROM songs WHERE album_id IN (
		SELECT a.id FROM albums as a
		INNER JOIN singersalbums as sa
		ON a.id = sa.album_id
		WHERE sa.singer_id = 3
	)
)
GROUP BY c.name;

SELECT a.name FROM albums AS a
JOIN singersalbums AS sa
ON a.id = sa.album_id
WHERE sa.singer_id IN (
	SELECT singer_id FROM singersgenders
	GROUP BY singer_id
	HAVING COUNT(gender_id) > 1
);

SELECT NAME FROM songs
WHERE id not IN (
	SELECT DISTINCT song_id FROM collectionssongs
);

SELECT s.name FROM singers as s
JOIN singersalbums as sa
ON s.id = sa.singer_id
WHERE sa.album_id IN (
	SELECT album_id FROM songs 
	WHERE LENGTH = (
		SELECT min(LENGTH) FROM songs
	)
);

SELECT NAME FROM albums
WHERE id IN (
	SELECT album_id FROM songs
	GROUP BY album_id
	HAVING COUNT(id) = (
		SELECT min(sel.songs_cnt) AS min_cnt FROM (
			SELECT album_id, COUNT(id) AS songs_cnt FROM songs
			GROUP BY album_id
		) 	AS sel
	)
);


