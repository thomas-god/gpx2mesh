from tempfile import NamedTemporaryFile

from src.db.con import ElevationDB


def test_insert_elevation_map():
    elevation = [(45, 5, 17), (46, 5, 167), (45, 6, 8), (46, 6, 12)]

    with NamedTemporaryFile("w+b") as db_file:
        db = ElevationDB(db_file.name)
        db.insert_elevation_map(elevation)

        with db.get_cursor() as cur:
            rows = cur.execute("SELECT lat, lon, elevation FROM elevation").fetchall()
            assert rows == elevation


def test_insert_elevation_map_no_duplicates():
    elevation_points = [(45, 5, 17), (46, 5, 167), (45, 6, 8), (46, 6, 12)]

    with NamedTemporaryFile("+at") as db_file:
        db = ElevationDB(db_file.name)
        db.insert_elevation_map(elevation_points)

        with db.get_cursor() as cur:
            new_points = [
                [
                    elevation_points[0][0],
                    elevation_points[0][1],
                    elevation_points[0][2] + 1,
                ]
            ]
            db.insert_elevation_map(new_points)

        with db.get_cursor() as cur:
            rows = cur.execute(
                "SELECT lat, lon, elevation FROM elevation ORDER BY lat, lon;"
            ).fetchall()
            assert len(rows) == len(elevation_points)
            assert rows[0] == elevation_points[0]


def test_load_existing_db():
    elevation_points = [(45, 5, 17), (46, 5, 167), (45, 6, 8), (46, 6, 12)]

    with NamedTemporaryFile("+at") as db_file:
        db = ElevationDB(db_file.name)
        db.insert_elevation_map(elevation_points)

        del db

        db_2 = ElevationDB(db_file.name)
        with db_2.get_cursor() as cur:
            rows = cur.execute(
                "SELECT lat, lon, elevation FROM elevation ORDER BY lat, lon;"
            ).fetchall()
            assert len(rows) == len(elevation_points)
