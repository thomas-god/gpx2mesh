from collections import namedtuple
from math import floor
from typing import Tuple
import xml.etree.ElementTree as ET
import numpy as np


TrackBounds = namedtuple("TrackBounds", ["lat_min", "lat_max", "lon_min", "lon_max"])


def load_track(trace_file: str) -> Tuple[np.ndarray, TrackBounds]:
    tree = ET.parse(trace_file)
    root = tree.getroot()
    track = root[1][2]

    lat_min = float(track[0].attrib["lat"])
    lat_max = float(track[0].attrib["lat"])
    lon_min = float(track[0].attrib["lon"])
    lon_max = float(track[0].attrib["lon"])
    trace = []

    for seg in track:
        lat = float(seg.attrib["lat"])
        lon = float(seg.attrib["lon"])

        trace.append((lon, lat))

        if lat < lat_min:
            lat_min = float(lat)
        if lat > lat_max:
            lat_max = float(lat)

        if lon < lon_min:
            lon_min = float(lon)
        if lon > lon_max:
            lon_max = float(lon)

    return np.array(trace), TrackBounds(
        lat_min=lat_min, lat_max=lat_max, lon_min=lon_min, lon_max=lon_max
    )


def trace_in_elev_coords(trace: np.ndarray, limits: TrackBounds, size):
    """

    Parameters
    - trace: numpy array of shape (n, 2), each row being (lon, lat)
    - limits:
    - size: size of the elevation array (assumed of shape (size, size))
    """

    def convert(a):
        lon, lat = a
        return np.array(
            [floor((lon - limits.lon_min) * size), floor((lat - limits.lat_min) * size)]
        )

    return np.apply_along_axis(convert, 1, trace)
