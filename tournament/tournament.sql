-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Clean out the old tables
DROP DATABASE IF EXISTS tournament;

-- (re)Create the new tables
CREATE database tournament;
\connect tournament;

CREATE TABLE players (
    id 			SERIAL PRIMARY KEY,
	full_name	TEXT
);

CREATE TABLE matches (
	winner		INTEGER REFERENCES players(id),
	loser		INTEGER REFERENCES players(id)
);

CREATE VIEW standings AS 
	SELECT 
		id, 
		full_name AS name,
		(SELECT COUNT(*) FROM matches WHERE winner = id) AS wins,
		(SELECT COUNT(*) FROM matches WHERE winner = id OR loser = id) AS matches
	FROM
		players;