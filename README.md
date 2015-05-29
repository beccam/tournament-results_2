Tournament Results
==================

## Summary
With the tournament.py module can be used to keep track of a Swiss tournament. This module
uses PostgresSQL database to track data such as players, matches and wins.Files included are:

* tournament.py - module to keep track of players during Swiss tournament style matches
* tournament_test.py - unit tests for the tournament.py module
* tournament.sql - this is the definition of the tables used in tournament.py

## Running the code

Run Postgres and create the tournament database
```
vagrant@vagrant-ubuntu-trusty-32:/vagrant/tournament$ psql
psql (9.3.6)
Type "help" for help.
vagrant=> CREATE DATABASE tournament;
```
Connect to the tournament database
```
vagrant=> \c tournament

```
Use the tables from tournament.sql in your database
```
tournament=> CREATE TABLE players (
tournament(>     id serial primary key,
tournament(>     name text
tournament(>     );

tournament=> CREATE TABLE matches(
tournament(> id SERIAL PRIMARY KEY,
tournament(> player_one_id INTEGER REFERENCES players,
tournament(> player_two_id INTEGER REFERENCES players,
tournament(> winner_id INTEGER REFERENCES players);
```
Run the unit test tournament_test.py
```
vagrant@vagrant-ubuntu-trusty-32:/vagrant/tournament$ python tournament_test.py
1. Old matches can be deleted.
2. Player records can be deleted.
3. After deleting, countPlayers() returns zero.
4. After registering a player, countPlayers() returns 1.
5. Players can be registered and deleted.
6. Newly registered players appear in the standings with no matches.
7. After a match, players have updated standings.
8. After one match, players with one win are paired.
Success!  All tests pass!
```
