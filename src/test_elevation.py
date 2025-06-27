import array
import struct
import tempfile
import numpy as np

from src.elevation import load_elevations_points
from src.trace import TrackBounds


def test_load_elevation_points():
    size = 3601
    with tempfile.NamedTemporaryFile(delete_on_close=False) as fp:
        for idx in range(7202):
            fp.write(struct.pack(">f", float(idx)))
        fp.close()

        elev = load_elevations_points(
            TrackBounds(lon_min=4.5, lon_max=4.6, lat_min=45.5, lat_max=45.6),
            file=fp.name,
        )

        # First row
        np.testing.assert_allclose(elev[0], [4, 46, 0])

        # First row, next to last element
        np.testing.assert_allclose(
            elev[size - 2], [4 + (size - 1) / size, 46, size - 2]
        )

        # End of first row
        np.testing.assert_allclose(elev[size - 1], [5, 46, size - 1])

        # Start of second row
        np.testing.assert_allclose(elev[size], [4, 46 - 1 / 3600, size])

        # End of second row
        np.testing.assert_allclose(elev[size * 2 - 1], [5, 46 - 1 / 3600, size * 2 - 1])
