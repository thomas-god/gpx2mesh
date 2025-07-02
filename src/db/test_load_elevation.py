import pytest
import numpy as np
from src.db.load_elevation import (
    ELEVATION_NAN_VALUE,
    IMAGE_SIZE,
    ElevationFilenameIncorrect,
    ElevationNotSquare,
    fill_nan_2d,
    parse_file,
    parse_file_name,
)


def test_number_of_points():
    elevations = parse_file("n45e004.hgts")

    assert len(elevations) == 3601 * 3601


def test_coordinates_parsing():
    elevations = parse_file("n45e004.hgts")

    first_point_of_first_row = elevations[0]
    assert first_point_of_first_row == (
        46,
        4,
        394,
    )  # Top-left corner of the tile, overlapping with next latitude tile

    second_point_of_first_row = elevations[1]
    assert second_point_of_first_row == (46, 4 + 1 / (IMAGE_SIZE - 1), 395)

    last_point_of_first_row = elevations[IMAGE_SIZE - 1]
    assert last_point_of_first_row == (
        46,
        5,
        331,
    )  # Last column overlaps with next longitude tile

    first_point_of_second_row = elevations[IMAGE_SIZE]
    assert first_point_of_second_row == (46 - 1 / (IMAGE_SIZE - 1), 4, 396)

    last_point = elevations[-1]
    assert last_point == (45, 5, 225)


def test_fill_nan_2d():
    elevations = [(45, 5, 17), (46, 5, 167), (45, 6, 8), (46, 6, np.nan)]

    filled_elevations = fill_nan_2d(elevations)
    nan_after = len([elev for (_, __, elev) in filled_elevations if np.isnan(elev)])

    assert nan_after == 0


def test_fill_nan_2d_raise_exception_arrray_not_square():
    elevations = [(46, 5, 167), (45, 6, 8), (46, 6, np.nan)]

    with pytest.raises(ElevationNotSquare):
        fill_nan_2d(elevations)


def test_replace_nanish_values():
    elevations = parse_file("n45e004.hgts")

    assert all((elev != ELEVATION_NAN_VALUE for (_, __, elev) in elevations))


def test_parse_file_name():
    assert parse_file_name("n45e004.hgts") == (45, 4)
    assert parse_file_name("n45w004.hgts") == (45, -4)
    assert parse_file_name("s45w004.hgts") == (-45, -4)

    with pytest.raises(ElevationFilenameIncorrect):
        parse_file_name("x45e004.hgts")
        parse_file_name("n45x004.hgts")
        parse_file_name("n4e004.hgts")
        parse_file_name("n456e004.hgts")
        parse_file_name("n45e04.hgts")
        parse_file_name("n456e0046.hgts")
