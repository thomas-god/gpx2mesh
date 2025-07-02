from tempfile import NamedTemporaryFile

from src.db.con import create_db, get_cursor, insert_elevation_map


def test_insert_elevation_map():
    elevation = [(45, 5, 17), (46, 5, 167), (45, 6, 8), (46, 6, 12)]

    with NamedTemporaryFile("+at") as db_file:
        create_db(db_file.name)

        with get_cursor(db_file.name) as cur:
            insert_elevation_map(elevation, cur)

        with get_cursor(db_file.name) as cur:
            rows = cur.execute("SELECT lat, lon, elevation FROM elevation").fetchall()
            assert rows == elevation


def test_insert_elevation_map_no_duplicates():
    elevation_points = [(45, 5, 17), (46, 5, 167), (45, 6, 8), (46, 6, 12)]

    with NamedTemporaryFile("+at") as db_file:
        create_db(db_file.name)

        with get_cursor(db_file.name) as cur:
            insert_elevation_map(elevation_points, cur)

        with get_cursor(db_file.name) as cur:
            new_points = [
                [
                    elevation_points[0][0],
                    elevation_points[0][1],
                    elevation_points[0][2] + 1,
                ]
            ]
            insert_elevation_map(new_points, cur)

        with get_cursor(db_file.name) as cur:
            rows = cur.execute(
                "SELECT lat, lon, elevation FROM elevation ORDER BY lat, lon;"
            ).fetchall()
            assert len(rows) == len(elevation_points)
            assert rows[0] == elevation_points[0]
