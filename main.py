import argparse
from src.elevation import (
    crop_elevation_map,
    load_elevation_map,
)
from src.mesh.track import add_gpx_track_to_terrain
from src.trace import load_track


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="elevation", description="Generate elevation mesh from gpc file"
    )
    parser.add_argument("-f", "--file")
    parser.add_argument("-d", "--debug", default=False)

    args = parser.parse_args()

    track, track_bounds = load_track(args.file)

    print(f"Track bounds: {track_bounds}")

    elevation = load_elevation_map(track_bounds)
    (elevation, [x_min, y_min], scale) = crop_elevation_map(elevation, track_bounds)
    track = (track - [x_min, y_min]) / [scale, scale]

    print("Generating mesh")
    mesh = add_gpx_track_to_terrain(elevation, track, track_bounds, debug=args.debug)

    mesh.export("elevation.stl")
    print("Mesh exported")