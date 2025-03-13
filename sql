-- FUNCTION: mediaserver.addsong(character varying, text, text, integer, text, integer)

-- DROP FUNCTION mediaserver.addsong(character varying, text, text, integer, text, integer);

CREATE OR REPLACE FUNCTION mediaserver.addsong(
	title character varying,
	description text,
	location text,
	length integer,
	genre text,
	artistid integer)
    RETURNS integer
    LANGUAGE 'sql'
    COST 100
    VOLATILE
AS $BODY$
WITH ins1 AS (
        INSERT INTO mediaserver.mediaItem(storage_location)
        VALUES (location)
        RETURNING media_id
        )
        ,ins2 AS (
        INSERT INTO mediaserver.metadata (md_type_id,md_value)
        SELECT md_type_id, description
        FROM mediaserver.MetaDataType where md_type_name = 'description'
        RETURNING md_id
        )
        ,ins3 AS (
        INSERT INTO mediaserver.audiomedia
        SELECT media_id FROM ins1
        )
        ,ins4 AS (
        INSERT INTO mediaserver.song
        SELECT media_id, title, length FROM ins1
        )
		,ins5 AS (
        INSERT INTO mediaserver.song_artists
        SELECT media_id, artistid FROM ins1
        )
        ,ins6 AS (
        INSERT INTO mediaserver.metadata (md_type_id, md_value)
        SELECT md_type_id, genre
        FROM mediaserver.MetaDataType where md_type_name = 'song genre'
        RETURNING md_id as genre_md_id
        )
        ,ins7 AS (
        INSERT INTO mediaserver.MediaItemMetaData
        SELECT media_id, genre_md_id FROM ins1, ins6
        )
        INSERT INTO mediaserver.MediaItemMetaData
        SELECT media_id, md_id FROM ins1, ins2;

        SELECT max(song_id) as song_id FROM mediaserver.song;
$BODY$;

ALTER FUNCTION mediaserver.addsong(character varying, text, text, integer, text, integer)
    OWNER TO y21s2i2120_<unikey>;

ALTER TABLE mediaserver.contactmethod
ADD UNIQUE(username, contact_type_id);

ALTER TABLE mediaserver.useraccount ALTER COLUMN password TYPE varchar (516);
ALTER TABLE mediaserver.useraccount ADD COLUMN salt text;

UPDATE mediaserver.useraccount
SET password = '289f01dd6d7c6cec5965bb38c3b24688dd10194c7200990c0bedf176c20e068e5b961cbe24fdeaf20cf6175c1962850427c669a67e64e6923518482e18602f88',
salt = '0962dc832f4d494d9d95dde6eb8a41d0'
where username LIKE 'james.smith';

INSERT INTO mediaserver.metadata
VALUES (7333, 6, 'comedy'),
(7334, 6, 'crime'),
(7335, 6, 'history'),
(7336, 6, 'drama'),
(7337, 6, 'educational'),
(7338, 6, 'interview'),
(7339, 6, 'news & politics'),
(7340, 6, 'thriller');

INSERT INTO mediaserver.podcastmetadata
VALUES(1, 7334),
(1, 7336),
(2, 7339),
(2, 7337),
(3, 7333),
(4, 7338),
(5, 7338),
(5, 7337),
(5, 7334),
(6, 7336),
(6, 7337),
(7, 7340),
(7, 7336),
(8, 7334),
(8, 7336),
(8, 7340),
(9, 7335),
(9, 7337),
(9, 7338),
(10, 7339),
(10, 7337),
(11, 7333),
(11, 7337),
(12, 7337),
(12, 7335),
(13, 7333);
