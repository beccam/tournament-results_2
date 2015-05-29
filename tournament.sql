-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE TABLE players (
    id serial primary key, 
    name text
    );

CREATE TABLE matches(
	id SERIAL PRIMARY KEY,
	player_one_id INTEGER REFERENCES players,
	player_two_id INTEGER REFERENCES players,
	winner_id INTEGER REFERENCES players);
