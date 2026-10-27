from __future__ import annotations
from pathlib import Path
from typing import Union, Any

# logging
import logging
logger = logging.getLogger(__name__)


#===================================================================================================
class Pather:
    #===============================================================================================
    def __init__(self, output_path: str, addon_path: str) -> None:
        """
        Initialize with two paths: output_path and addon_path. Both paths may contain
        string format placeholders, and addon_path will be appended to output_path.
        """
        self.original_addon_path: Path = Path(addon_path)
        self.output_path        : Path = Path(output_path)
        self.complete_path      : Path = self.output_path / self.original_addon_path
        return
    #===============================================================================================

    #===============================================================================================
    def add_to_general_path(self, extra_path: str) -> None:
        """
        Extend the complete_path by appending extra_path to it.
        """
        self.complete_path /= Path(extra_path)
        return
    #===============================================================================================

    #===============================================================================================
    def set_params(self, params: dict[str, Union[str, int, float]]) -> None:
        """
        Format the paths using the provided dictionary of parameters.
        Updates both complete_path and original_addon_path with the formatted values.
        """
        # Format the paths using the dictionary of params
        self.complete_path = Path(str(self.complete_path).format(**params))
        self.original_addon_path = Path(str(self.original_addon_path).format(**params))
        return
    #===============================================================================================

    #===============================================================================================
    def get_path(self, extra: Union[None, str, Path, 'Pather'] = None) -> 'Pather':
        """
        Return a new Pather object based on the current complete path, optionally appending another path.
        Creates the directory if it doesn't exist.
        """
        # Handle the case where extra path is provided
        if extra:
            if isinstance(extra, Pather):
                new_path = self.complete_path / extra.complete_path
            else:
                new_path = self.complete_path / Path(extra)
        else:
            new_path = self.complete_path

        # Create the directory if it doesn't exist
        self._create_dir(new_path)

        # Return a new Pather object with the updated path
        return Pather(str(self.output_path), str(new_path.relative_to(self.output_path)))
    #===============================================================================================

    #===============================================================================================
    @property
    def path(self) -> str:
        return str(self.complete_path)
    #===============================================================================================

    #===============================================================================================
    def _create_dir(self, path: Path) -> None:
        """
        Create the directory if it doesn't exist.
        """
        # if not path.is_dir():
        if '.' not in str(path):
            logger.debug(f'Creating path {path.parent}')
            path.mkdir(parents=True, exist_ok=True)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
        return
    #===============================================================================================

    #===============================================================================================
    # Proxy methods to behave like a Path object
    def __getattr__(self, name: str) -> Any:
        """Delegate attribute access to the current Path object."""
        return getattr(self.complete_path, name)
    #===============================================================================================

    #===============================================================================================
    def __str__(self) -> str:
        """Return string representation of the current path."""
        return str(self.complete_path)
    #===============================================================================================

    #===============================================================================================
    def __fspath__(self) -> str:
        """For compatibility with os functions, return the file system path."""
        return str(self.complete_path)
    #===============================================================================================

    #===============================================================================================
    def __truediv__(self, other: Union[str, Path, 'Pather']) -> 'Pather':
        """
        Overload the `/` operator to join paths like Path objects.
        """
        if isinstance(other, Pather):
            new_path = self.complete_path / other.complete_path
        else:
            new_path = self.complete_path / other

        self._create_dir(new_path)
        return Pather(str(self.output_path), str(new_path.relative_to(self.output_path)))
    #===============================================================================================

    #===============================================================================================
    def __rtruediv__(self, other: Union[str, Path, 'Pather']) -> 'Pather':
        """
        Reverse division to support joining paths the other way.
        """
        if isinstance(other, Pather):
            new_path = other.complete_path / self.complete_path
        else:
            new_path = Path(other) / self.complete_path

        self._create_dir(new_path)
        return Pather(str(self.output_path), str(new_path.relative_to(self.output_path)))
    #===============================================================================================

    #===============================================================================================
    def __add__(self, other: Union[str, Path, Pather]) -> Pather:

        if isinstance(other, Pather):
            new_path = Path(str(self.complete_path) + str(other.complete_path))
        elif isinstance(other, Path):
            new_path = Path(str(self.complete_path) + str(other))
        else:
            new_path = Path(str(self.complete_path) + other)

        return Pather(str(self.output_path), str(new_path.relative_to(self.output_path)))
    #===============================================================================================

    #===============================================================================================
    def __radd__(self, other: Union[str, Path, Pather]) -> Pather:

        if isinstance(other, Pather):
            new_path = Path(str(other.complete_path) + str(self.complete_path))
        elif isinstance(other, Path):
            new_path = Path(str(other) + str(self.complete_path))
        else:
            new_path = Path(other + str(self.complete_path))

        return Pather(str(self.output_path), str(new_path.relative_to(self.output_path)))
    #===============================================================================================
#===================================================================================================


if __name__ == "__main__":
    from tempfile import TemporaryDirectory

    with TemporaryDirectory(prefix="pather_example_") as temporary_dir:
        outputs = Pather(temporary_dir, "run_{number}")
        outputs.set_params({"number": 42})

        report = outputs / "summary.txt"
        report.write_text("done\n")

        plots = outputs.get_path("plots")
        print(f"Report: {report.path}")
        print(f"Plots directory: {plots.path}")
