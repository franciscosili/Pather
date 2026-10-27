# Pather

`Pather` is a small wrapper around `pathlib.Path` for building output paths. It joins a base output directory with an additional path, fills in `{name}` placeholders, and creates directories when you request a path.

## Requirements and setup

- Python 3.9 or newer
- No third-party dependencies

The repository is a single module, with no package installer. Keep `Pather.py` in your project or add this repository to your Python import path, then import it with `from Pather import Pather`.

## Quick start

```python
from Pather import Pather

outputs = Pather("results", "run_{number}")
outputs.set_params({"number": 42})

report = outputs / "summary.txt"  # Creates results/run_42/
report.write_text("done\n")       # Delegated to pathlib.Path

print(report.path)                  # results/run_42/summary.txt
```

`get_path()` also returns a new `Pather` and creates the directory:

```python
plots = outputs.get_path("plots")
print(plots.path)  # results/run_42/plots
```

Run the example in the module with `python3 Pather.py`. It writes a report in a temporary directory, prints the report and plots paths, and removes the temporary directory when it exits.

## API

| Member | Behavior |
| --- | --- |
| `Pather(output_path, addon_path)` | Joins the two paths. Both arguments are strings. Put format placeholders in `addon_path`. |
| `set_params(params)` | Applies `str.format(**params)` to the current path and the original additional path. Values may be strings, integers, or floats. |
| `add_to_general_path(extra_path)` | Appends a path to the current `Pather` in place. |
| `get_path(extra=None)` | Creates the requested path or its parent directory and returns a new `Pather`. |
| `pather / extra` | Joins a path, creates the requested path or its parent directory, and returns a new `Pather`. |
| `pather + suffix` | Concatenates path text and returns a new `Pather`; it does not create directories. |
| `path` | Returns the current path as a string. |

The object also supports `str(pather)`, `os.fspath(pather)`, and access to `pathlib.Path` attributes and methods such as `write_text()` and `exists()`.

## Path creation behavior

`get_path()` and `/` decide whether to create a directory or only its parent by checking for a dot (`.`) anywhere in the resulting path string. A dotted directory name in any part of the path therefore causes only the parent to be created. If that path is meant to be a directory, create it explicitly with `Path(pather.path).mkdir(parents=True, exist_ok=True)`.

Joined paths should remain inside `output_path`: operations that produce a path outside it raise `ValueError` when the result is made relative to the base path.

Keep `output_path` unformatted. `set_params()` formats the current path but leaves the stored base path unchanged, which can make later joins fail if the base contains placeholders.
