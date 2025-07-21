from math import ceil, floor
import struct
import numpy as np
from scipy import ndimage
from scipy.ndimage import gaussian_filter

from src.trace import TrackBounds

ELEVATION_NAN_VALUE = -32768


def find_elevation_file(track_bounds: TrackBounds):
    return f"n{floor(track_bounds.lat_min)}e{floor(track_bounds.lon_min):>03}.hgts"


def load_elevation_map(track_bounds: TrackBounds) -> np.ndarray:
    """
    Load elevation values from file, interpolate missing values, and apply a gaussian filter.
    """
    file = find_elevation_file(track_bounds)
    print(f"loading elevation from file {file}")
    size = 3601

    elev = np.fromfile(file, dtype=">f4")
    elev = np.where(elev == ELEVATION_NAN_VALUE, np.nan, elev)
    elev = elev.reshape((size, size))

    nan_mask = np.isnan(elev)
    _, indices = ndimage.distance_transform_edt(nan_mask, return_indices=True)
    elev[nan_mask] = elev[tuple(indices[:, nan_mask])]

    elev = gaussian_filter(elev, sigma=3, radius=4)

    return elev


def crop_elevation_map(elevation: np.ndarray, track_bounds: TrackBounds):
    """
    Crop an elevation map to fit the track bounds. Returns the crop map together with
    the coordinate shift vector.
    """
    rows, cols = elevation.shape
    assert rows == cols
    size = rows

    width_c = (
        max(
            track_bounds.lon_max - track_bounds.lon_min,
            track_bounds.lat_max - track_bounds.lat_min,
        )
        * 1.2
    )

    mid_lat = (track_bounds.lat_max + track_bounds.lat_min) / 2
    cropped_lat_min = mid_lat - width_c / 2
    cropped_lat_max = mid_lat + width_c / 2
    row_min = floor((1 - (cropped_lat_max % 1)) * size)
    row_max = ceil((1 - (cropped_lat_min % 1)) * size)

    mid_lon = (track_bounds.lon_max + track_bounds.lon_min) / 2
    cropped_lon_min = mid_lon - width_c / 2
    cropped_lon_max = mid_lon + width_c / 2
    col_min = floor((cropped_lon_min % 1) * size)
    col_max = ceil((cropped_lon_max % 1) * size)

    print(row_min, row_max, col_min, col_max)

    cropped_elevation = elevation[
        row_min:row_max,
        col_min:col_max,
    ]
    shift_vector = [cropped_lon_min, cropped_lat_min]
    print(f"shift vector: {shift_vector}")
    return (cropped_elevation, shift_vector, width_c)


def load_elevations_points(track_bounds: TrackBounds, file=None):
    if file is None:
        file = find_elevation_file(track_bounds)
    lon_min = floor(track_bounds.lon_min)
    lat_max = ceil(track_bounds.lat_max)

    print(f"loading elevation from file {file}")
    size = 3601
    elev = []
    idx = 0

    with open(file, "rb") as f:
        while bytes := f.read(4):
            val = struct.unpack(">f", bytes)[0]
            val = np.nan if val == ELEVATION_NAN_VALUE else val
            lon = lon_min + (idx % size) / (size - 1)
            lat = lat_max - (idx // size) / size
            elev.append([lon, lat, val])
            idx += 1

    return np.array(elev)


def crop_elevation_points(points: np.ndarray, bounds: TrackBounds):
    mask = np.ones(len(points), dtype=bool)

    mask &= points[:, 0] >= bounds.lon_min
    mask &= points[:, 0] <= bounds.lon_max
    mask &= points[:, 1] <= bounds.lat_max
    mask &= points[:, 1] <= bounds.lat_max

    return points[mask]
