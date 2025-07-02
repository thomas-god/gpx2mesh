import contextlib
import sqlite3


class ElevationDB:
    def __init__(self, filename: str):
        self.con = sqlite3.connect(filename)
        self.init_db()

    def __del__(self):
        self.con.close()

    def init_db(self):
        cur = self.con.cursor()

        tables = cur.execute("SELECT name FROM sqlite_master").fetchall()

        if ("elevation",) in tables:
            return

        cur.execute("CREATE TABLE elevation(lat, lon, elevation);")
        cur.execute(
            "CREATE UNIQUE INDEX elevation_unique_lat_lon ON elevation(lat, lon)"
        )

        self.con.commit()

    @contextlib.contextmanager
    def get_cursor(self):
        cur = self.con.cursor()

        yield cur
        self.con.commit()

    def insert_elevation_map(self, elevation):
        cur = self.con.cursor()
        cur.executemany(
            """INSERT INTO elevation VALUES(?,?,?)
        ON CONFLICT(lat, lon) DO NOTHING""",
            elevation,
        )
        self.con.commit()
