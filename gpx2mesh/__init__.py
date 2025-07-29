from gpx2mesh.elevation import (
    crop_elevation_map,
    load_elevation_map,
)
from gpx2mesh.mesh import generate_mesh
from gpx2mesh.trace import load_track


def build_mesh(filename: str, debug=False):
    track, track_bounds = load_track(filename)

    print(f"Track bounds: {track_bounds}")

    elevation = load_elevation_map(track_bounds)
    (elevation, [x_min, y_min], scale) = crop_elevation_map(elevation, track_bounds)
    track = (track - [x_min, y_min]) / [scale, scale]

    print("Generating mesh")
    mesh = generate_mesh(elevation, track, width=50, debug=debug)

    mesh.merge_vertices()

    return mesh
