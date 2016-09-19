#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM matches;")
    c.execute("update standings set wins =0, matches=0")
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM players;")
    c.execute("DELETE FROM matches;")
    c.execute("DELETE FROM standings;")
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT count(player_id) FROM players;")
    number = c.fetchall()[0][0]
    conn.close()
    return number


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    c = conn.cursor()
    c.execute("insert into players (name) values (%s);", (name,))
    c.execute("select max(player_id) from players;")
    id = c.fetchall()[0][0]
    c.execute(
        "insert into standings (player_id, wins, matches) values (%s, 0, 0);", (id,))
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
    conn = connect()
    c = conn.cursor()
    query = "select players.player_id, players.name, standings.wins, standings.matches from players left join standings on players.player_id = standings.player_id order by standings.wins DESC"
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
    conn = connect()
    c = conn.cursor()
    c.execute("insert into matches (winner, loser) values (%s, %s);",
              (winner, loser,))
    c.execute(
        "update standings set wins=wins+1 , matches =matches +1 where player_id = (%s);", (
            winner,))
    c.execute(
        "update standings set matches =matches +1  where player_id = (%s);", (
            loser,))
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
    #[id1, id2, id3, id4, id5, id6, id7, id8] = [row[0] for row in standings]
    conn = connect()
    c = conn.cursor()
    c.execute("select players.player_id, players.name from players left join standings on players.player_id = standings.player_id order by standings.wins DESC")
    player_list = [(row[0], row[1])
                   for row in c.fetchall()]
    conn.close()
    match_list = [(player_list[i][0], player_list[i][1], player_list[
                   i + 1][0], player_list[i + 1][1]) for i in range(0, len(player_list), 2)]
    return match_list


'''
to-do list:


    Prevent rematches between players.

    Don’t assume an even number of players. If there is an odd number of players, assign one player a “bye” (skipped round). A bye counts as a free win. A player should not receive more than one bye in a tournament.

    Support games where a draw (tied game) is possible. This will require changing the arguments to reportMatch.

    When two players have the same number of wins, rank them according to OMW (Opponent Match Wins), the total number of wins by players they have played against.

    Support more than one tournament in the database, so matches do not have to be deleted between tournaments. This will require distinguishing between “a registered player” and “a player who has entered in tournament #123”, so it will require changes to the database schema.
    
    You may refer to outside resources to devise your pairing algorithm. Wizards of the Coast has prepared simple instructions, and more details can be found in resources linked to in the reference section of Wikipedia's article on Swiss tournaments.
'''
