-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
CREATE TABLE players ( name TEXT, player_id SERIAL PRIMARY KEY );

CREATE TABLE matches ( winner integer, 
loser integer , match_id SERIAL PRIMARY KEY);

CREATE TABLE standings ( player_id integer, wins integer,
matches integer);

-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


