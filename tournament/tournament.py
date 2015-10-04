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
    # Open database connection
    db = connect()
    cursor = db.cursor()
    # Delete Matches
    cursor.execute("DELETE FROM matches;")
    db.commit()
    # Close database connection
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    # Open database connection
    db = connect()
    cursor = db.cursor()
    # Delete Players
    cursor.execute("DELETE FROM players;")
    db.commit()
    # Close database connection
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    # Open database connection
    db = connect()
    cursor = db.cursor()
    # Count Players
    cursor.execute("SELECT COUNT(*) FROM players;")
    retval = cursor.fetchone()[0]
    db.commit()
    # Close database connection
    db.close()
    return retval


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    cursor = db.cursor()
    cursor.execute("INSERT INTO players (full_name) VALUES (%s);", (name,))
    db.commit()
    db.close()


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
    db = connect()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM standings;")
    retval = cursor.fetchall()
    db.close()
    return retval


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    # Open database connection
    db = connect()
    cursor = db.cursor()
    # Insert Match
    cursor.execute("INSERT INTO matches (winner, loser) VALUES (%s, %s);",
                   (winner, loser))
    db.commit()
    # Close database connection
    db.close()


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
    if countPlayers() % 2 == 1:
        raise ValueError("Odd number of players!")
    db = connect()
    cursor = db.cursor()
    # Get a list of players sorted by wins.
    cursor.execute("SELECT * FROM standings")
    playerList = cursor.fetchall()
    matches = []
    # Now that we have a sorted list, assign each player to their neighbor
    for i in xrange(0, len(playerList), 2):
        matches.append(
            (playerList[i][0],
             playerList[i][1],
             playerList[i+1][0],
             playerList[i+1][1]))
    return matches
