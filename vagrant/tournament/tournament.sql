-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--

DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament

CREATE TABLE players ( name TEXT, player_id SERIAL PRIMARY KEY );

CREATE TABLE matches ( winner integer REFERENCES  players(player_id), 
loser integer REFERENCES  players(player_id), match_id SERIAL PRIMARY KEY);

CREATE VIEW wins as
 SELECT player_id, CASE WHEN number_wins IS NULL THEN 0 ELSE number_wins END
 FROM players LEFT JOIN
 ( SELECT winner, count(match_id) as number_wins
 FROM matches
 GROUP by winner) AS win
 on players.player_id = win.winner;

CREATE VIEW loses as
 SELECT player_id, CASE WHEN number_loses IS NULL THEN 0 ELSE number_loses END
 FROM players LEFT JOIN
 ( SELECT loser , count(match_id) as number_loses
 FROM matches
 GROUP by loser) AS lose
  on players.player_id = lose.loser;

CREATE VIEW standings as
(SELECT players.player_id, number_wins as wins, number_wins+number_loses as matches
FROM players LEFT JOIN wins
ON players.player_id = wins.player_id
LEFT JOIN loses
ON players.player_id = loses.player_id)



--CASE WHEN number_wins+number_loses IS NULL THEN 0 ELSE number_wins+number_loses  END as matches
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


