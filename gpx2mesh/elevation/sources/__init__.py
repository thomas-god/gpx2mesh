import abc
import os
from pathlib import Path
from typing import List


class ElevationFileNotFoundError(Exception):
    def __init__(self, missing_files: List[str]):
        self.missing_files = missing_files


class IGetElevationFiles(metaclass=abc.ABCMeta):
    """Provide host-dependant path of elevation files."""

    @abc.abstractmethod
    def get_paths(self, files: List[str]) -> List[Path]:
        """May raise ElevationFileNotFound if a file cannot be found."""
        pass


class AssetsFolderProvider(IGetElevationFiles):
    """Provide elevation file location from a given assets folder."""

    def __init__(self, assets: Path):
        self.assets = assets

    def get_paths(self, files):
        """Raise ElevationFileNotFoundError if some files cannot be found."""

        paths = []
        missing_files = []

        for file in files:
            if os.path.exists(self.assets / file):
                paths.append(self.assets / file)
            else:
                missing_files.append(file)

        if len(missing_files) > 0:
            raise ElevationFileNotFoundError(missing_files)

        return paths
