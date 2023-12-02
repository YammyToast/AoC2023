from dataclasses import dataclass
from time import *
import re

from pathlib import Path
working_dir = Path().absolute()
profiler_path = Path(__file__)


@dataclass
class PythonFileProfile:
    _file_py: str
    _parent_dir: str
    _lines: int
    _process_time_ms: int
    _imports: list[str]
    _full_file_path: Path


def count_file_lines(__file_path):
    c = 0
    with open(__file_path) as f:
        for line in f:
            # Don't count blank lines
            c += (not line.isspace())
    return c


def collect_imports(__file_path):
    imports = []
    with open(__file_path) as f:
        for line in f:
            # Pattern from: https://stackoverflow.com/a/53635205
            if (x:= re.search(r"^\s*(?:from|import)\s+(\w+(?:\s*,\s*\w+)*)", line)) != None:
                # group(1) extracts the library name. god-bless python regex.
                imports.append(x.group(1))
    return imports




def get_profiles(__file_path_list: list[Path]):
    profiles = []
    for file in __file_path_list:
        profiles.append(PythonFileProfile(
            _file_py=file.parts[-1],
            _parent_dir=file.parts[-2],
            _lines=count_file_lines(file),
            _process_time_ms=None,
            _imports=collect_imports(file),
            _full_file_path=file
        ))
    return profiles


def main():
    # Remove profiler from the profiler.
    all_python_file_list = list(
        filter(lambda x: x != profiler_path, working_dir.rglob("*.py")))

    profiles = get_profiles(all_python_file_list)
    print(profiles)


if __name__ == '__main__':
    main()
