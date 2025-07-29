import io
from itertools import product
from math import floor
import os
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import List
from dotenv import dotenv_values
import requests
import zipfile

from gpx2mesh.trace import TrackBounds


config = dotenv_values(".env")


def get_filenames(bounds: TrackBounds) -> List[str]:
    return [
        _map_filename(lat, lon)
        for lat, lon in product(
            range(floor(bounds.lat_min), floor(bounds.lat_max + 1)),
            range(floor(bounds.lon_min), floor(bounds.lon_max + 1)),
        )
    ]


def _map_filename(lat: int, lon: int) -> str:
    _lat = f"{'n' if lat >= 0 else 's'}{abs(floor(lat)):>02}"
    _lon = f"{'e' if lon >= 0 else 'w'}{abs(floor(lon)):>03}"

    return _lat + _lon + ".hgts"


def get_files(files: List[str]):
    print(f"Checking files {files} in {config['ASSETS']}")
    os.makedirs(config["ASSETS"], exist_ok=True)

    missing_files = [
        file
        for file in files
        if not os.path.isfile(os.path.join(config["ASSETS"], file))
    ]

    if len(missing_files) == 0:
        return

    print(f"{len(missing_files)} elevation files need to be downloaded")

    with requests.Session() as session:
        session.auth = (config["LOGIN"], config["PWD"])

        for file in files:
            filename = file.removesuffix(".hgts")
            url = f"{config['URL_PREFIX']}/NASADEM_SHHP_{filename}/NASADEM_SHHP_{filename}.zip"
            r1 = session.request("get", url)

            r = session.get(r1.url, auth=(config["LOGIN"], config["PWD"]))

            if r.ok:
                z = zipfile.ZipFile(io.BytesIO(r.content))
                with TemporaryDirectory() as tmpdir:
                    z.extractall(tmpdir)
                    Path(os.path.join(tmpdir, file)).rename(
                        os.path.join(config["ASSETS"], file)
                    )
                    print(f"Downloaded elevation file {file}")

            else:
                print(
                    f"Error when trying to download {file}: response has {r.status_code}"
                )
