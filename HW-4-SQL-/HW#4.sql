SELECT COUNT(musiciansstyle.musical_style_id) cms, musical_style.style_name mstn FROM musical_style
LEFT JOIN musiciansstyle ON musical_style.musical_style_id = musiciansstyle.musical_style_id
LEFT JOIN musicians m ON musiciansstyle.musicians_id = m.musicians_id
GROUP BY mstn
ORDER BY  cms DESC;

SELECT COUNT(tracks.name) FROM tracks
JOIN albums ON tracks.album = albums.albums_id
WHERE release_date BETWEEN  '2019-01-01' and '2020-12-31';

SELECT AVG(t.duration), albums.name an FROM tracks t
JOIN albums ON t.album = albums.albums_id
GROUP BY an;

SELECT m.name FROM musicians m
WHERE m.name NOT IN (
SELECT musicians.name FROM musicians
JOIN musiciansalbums ON musicians.musicians_id = musiciansalbums.musicians_id
JOIN albums a ON musiciansalbums.albums_id = a.albums_id
WHERE release_date BETWEEN  '2020-01-01' and '2020-12-31'
);

SELECT DISTINCT collections.name  FROM collections
JOIN collectiontrack ON collections.collection_id = collectiontrack.collection_id
JOIN tracks t ON collectiontrack.tracks_id = t.tracks_id
JOIN albums a ON t.album = a.albums_id
JOIN musiciansalbums ma ON a.albums_id = ma.albums_id
JOIN musicians m ON ma.musicians_id = m.musicians_id
WHERE m.name = 'Mozart';

--INSERT INTO musiciansalbums (albums_id, musicians_id)
--VALUES 
--(1,6);

SELECT albums.name an FROM albums
JOIN musiciansalbums ON albums.albums_id = musiciansalbums.albums_id
JOIN musicians m ON musiciansalbums.musicians_id = m.musicians_id
JOIN musiciansstyle ms ON m.musicians_id = ms.musicians_id
JOIN musical_style mst ON ms.musical_style_id = mst.musical_style_id
GROUP BY an
HAVING COUNT(DISTINCT  mst.style_name) > 1;

--INSERT INTO Tracks (name, duration, album)
--VALUES 
--('LOVE', 222, 6)

SELECT t.name FROM tracks t
WHERE t.tracks_id NOT IN (
    SELECT tracks_id FROM collectiontrack
    );

SELECT m.name FROM musicians m
JOIN musiciansalbums ma ON m.musicians_id = ma.musicians_id
JOIN albums a ON ma.albums_id = a.albums_id
JOIN tracks t ON a.albums_id = t.album
WHERE t.duration = (
	SELECT MIN(duration) FROM tracks
	);

SELECT a.name FROM albums AS a
JOIN tracks AS t ON t.album  = a.albums_id
WHERE t.album IN (
    SELECT album FROM tracks
    GROUP BY album
    HAVING COUNT(album) = (
        SELECT COUNT(album) FROM tracks
        GROUP BY album
        ORDER BY count
        LIMIT 1 )
        );

