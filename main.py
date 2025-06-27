import argparse
from src.elevation import (
    crop_elevation_map,
    load_elevation_map,
)
from src.mesh import elevation_to_mesh
from src.trace import load_track


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="elevation", description="Generate elevation mesh from gpc file"
    )
    parser.add_argument("-f", "--file")

    args = parser.parse_args()

    print(args)

    trace, trace_bounds = load_track(args.file)

    elevation = load_elevation_map(trace_bounds)
    (elevation, _) = crop_elevation_map(elevation, trace_bounds)

    print(elevation.shape)

    mesh = elevation_to_mesh(elevation)

    mesh.export("elevation.stl")
