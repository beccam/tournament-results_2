#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    """ Will connect with the tournament database. """
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    """ Will clear out the matches table in the database. """
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM matches")
    conn.commit()
    conn.close()

def deletePlayers():
    """Remove all the player records from the database."""
    """Will remove the players from the players table in the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM players")
    conn.commit()
    conn.close()

def countPlayers():
    """Returns the number of players currently registered."""
    """Will return number of players in the players table. """
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT count(*) AS num_players FROM players;")
    num_players = c.fetchone()
    conn.close()
    return num_players[0]

def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    """ Adds a player to the players table."""
    conn = connect()
    c = conn.cursor()
    c.execute("INSERT INTO players (name) VALUES (%s)", (name,))
    conn.commit()
    conn.close()

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    """Will return a list of players and wins, sorted by most wins."""
    conn = connect()
    c = conn.cursor()
    c.execute("""
    SELECT x0.id as id, x0.name as name, COALESCE(win, 0) wins, COALESCE(matches_played, 0) as matches
    FROM
    (SELECT id, name from players) x0
    LEFT OUTER JOIN
    (SELECT p1.id as id1, p1.name as name, count(m1.id) as matches_played
      FROM players as p1, matches as m1
      WHERE p1.id = m1.player_one_id OR p1.id = m1.player_two_id
      GROUP BY p1.id) x1
    ON (x0.id = x1.id1)
    LEFT OUTER JOIN
      (SELECT count(*) as win, p2.id as id2
      FROM matches as m2, players as p2
      WHERE (p2.id = m2.winner_id)
      GROUP BY p2.id) x2
    ON (x1.id1 = x2.id2)
    ORDER BY wins DESC, matches DESC;""")
    return c.fetchall()

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    """Will return the result of a single match between two players."""
    conn = connect()
    c = conn.cursor()
    sql = '''
    INSERT INTO matches(player_one_id,player_two_id,winner_id)
    VALUES(  %s  , %s  ,   %s  );''' % ( str(winner) , str(loser) , str(winner))
    c.execute(sql)
    conn.commit()
    conn.close()

def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    """Will return a list of players for the next round according to the Swiss
    pairing style."""
    rows = playerStandings()
    pairs = []
    for (i, j) in zip(rows, rows[1::])[::2]:
        pair = (i[0], i[1], j[0], j[1])
        pairs.append(pair)
    return pairs
