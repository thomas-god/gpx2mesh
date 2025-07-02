from math import sqrt
import re
import struct
from typing import List, Tuple
import numpy as np
from scipy.interpolate import griddata

IMAGE_SIZE = 3601
ELEVATION_NAN_VALUE = -32768


def load_elevation(file_name: str):
    """Load elevation data into DB from an elevation file."""
    elevation = parse_file(file_name)

    return elevation


class ElevationNotSquare(Exception):
    """Elevation map is expected to be a square, i.e. len(map) is as square number"""

    pass


def fill_nan_2d(points) -> np.array:
    size = int(sqrt(len(points)))
    if len(points) != size * size:
        raise ElevationNotSquare

    points = np.array(points).reshape((size, size, 3))

    valid_mask = ~np.isnan(points)
    valid_rows = valid_mask[:, :, 2]
    valid_points = np.column_stack([points[valid_rows][:, 0], points[valid_rows][:, 1]])
    valid_values = points[valid_rows][:, 2]

    nan_mask = np.isnan(points)
    nan_rows = nan_mask[:, :, 2]
    nan_points = np.column_stack([points[nan_rows][:, 0], points[nan_rows][:, 1]])

    interpolated_values = griddata(
        valid_points, valid_values, nan_points, method="nearest"
    )

    print(
        f"Number of nan to interpolate: {len(interpolated_values)}/{size * size} total points"
    )

    points[nan_mask] = interpolated_values

    return points.reshape((size * size, 3)).tolist()


def parse_file(file_name: str) -> List[Tuple[float, float, int]]:
    """Parse data from an elevation file as a list of (latitude, longitude, elevation)."""
    (lat_min, lon_min) = parse_file_name(file_name)
    lat_max = lat_min + 1
    points = []

    idx = 0
    with open(file_name, "rb") as file:
        while bytes := file.read(4):
            lat = lat_max - (idx // IMAGE_SIZE) / (IMAGE_SIZE - 1)
            lon = lon_min + (idx % IMAGE_SIZE) / (IMAGE_SIZE - 1)
            value = int(struct.unpack(">f", bytes)[0])
            value = np.nan if value == ELEVATION_NAN_VALUE else value
            points.append((lat, lon, value))

            idx += 1

    return points


class ElevationFilenameIncorrect(Exception):
    """Filename does not match pattern (n|s)(\d{2})(e|w)(\d{3}).hgts for elevation files."""

    pass


def parse_file_name(file_name: str) -> Tuple[int]:
    """Parse (lat, lon) of the bottom left point."""

    if re.match("(n|s)(\d{2})(e|w)(\d{3}).hgts", file_name) is None:
        raise ElevationFilenameIncorrect

    north_south = file_name[0]
    lat = int(file_name[1:3])
    east_west = file_name[3]
    lon = int(file_name[4:7])

    if north_south == "s":
        lat *= -1

    if east_west == "w":
        lon *= -1

    return (lat, lon)
