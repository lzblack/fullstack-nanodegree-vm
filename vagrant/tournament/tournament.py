#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect(database_name="tournament"):
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        return db, cursor
    except:
        print("Connection fails.")


def deleteMatches():
    """Remove all the match records from the database."""
    conn, c = connect()
    c.execute("DELETE FROM matches;")
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn, c = connect()
    c.execute("DELETE FROM players;")
    c.execute("DELETE FROM matches;")
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    conn, c = connect()
    query = "SELECT count(player_id) FROM players;"
    c.execute(query)
    number = c.fetchone()[0]
    conn.close()
    return number


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """

    conn, c = connect()
    query = "INSERT INTO players (name) VALUES (%s);"
    parameter = (name,)
    c.execute(query, parameter)
    conn.commit()
    conn.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a
    player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn, c = connect()
    query = "select players.player_id, players.name, standings.wins, standings.matches \
    from players left join standings \
    on players.player_id = standings.player_id \
    order by standings.wins DESC"
    c.execute(query)
    standings = [(row[0], row[1], row[2], row[3])
                 for row in c.fetchall()]
    conn.close()
    return standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn, c = connect()
    query = "insert into matches (winner, loser) values (%s, %s);"
    c.execute(query, (winner, loser,))
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
    standings = playerStandings()
    conn, c = connect()
    query = "select players.player_id, players.name from players \
    left join standings on players.player_id = standings.player_id \
    order by standings.wins DESC"
    c.execute(query)
    player_list = [(row[0], row[1])
                   for row in c.fetchall()]
    conn.close()
    match_list = [(player_list[i][0], player_list[i][1], player_list[
                   i + 1][0], player_list[i + 1][1])
                  for i in range(0, len(player_list), 2)]
    return match_list
