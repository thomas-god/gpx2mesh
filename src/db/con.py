import contextlib
import sqlite3


def create_db(filename: str = "elevation.db"):
    """Create and initialise elevation sqlite database."""

    con = sqlite3.connect(filename)

    cur = con.cursor()

    cur.execute("CREATE TABLE elevation(lat, lon, elevation);")
    cur.execute("CREATE UNIQUE INDEX elevation_unique_lat_lon ON elevation(lat, lon)")

    con.commit()

    con.close()


@contextlib.contextmanager
def get_cursor(db: str = "elevation.db"):
    """Yield a cursor to the db and commit pending transactions before closing the transaction"""

    con = sqlite3.connect(db)

    cur = con.cursor()

    try:
        yield cur
        con.commit()
    finally:
        con.close()


def insert_elevation_map(elevation, cur: sqlite3.Cursor):
    cur.executemany(
        """INSERT INTO elevation VALUES(?,?,?)
        ON CONFLICT(lat, lon) DO NOTHING""",
        elevation,
    )
