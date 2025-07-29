import argparse
import re

from gpx2mesh import build_mesh


def main():
    parser = argparse.ArgumentParser(
        prog="elevation", description="Generate elevation mesh from a .gpx file"
    )
    parser.add_argument("-f", "--file")
    parser.add_argument("-d", "--debug", default=False)

    args = parser.parse_args()

    mesh = build_mesh(args.file, debug=args.debug)

    export_file = re.sub(r"\.gpx$", ".stl", args.file)
    mesh.export(export_file)
    print(f"Mesh exported in {export_file}")


if __name__ == "__main__":
    main()
