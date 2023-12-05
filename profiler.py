from dataclasses import dataclass
import time
import re
from mdutils.mdutils import MdUtils
import itertools
import os
import importlib.util
import sys

from pathlib import Path

working_dir = Path().absolute()
profiler_path = Path(__file__)

comment_pattern = re.compile(r"^[\s]*#[\s\w]*$", re.DOTALL)


@dataclass
class PythonFileProfile:
    _file_py: str
    _parent_dir: str
    _lines: int
    _process_time_ms: int
    _imports: list[str]
    _full_file_path: str


def is_comment(__line: str):
    return re.match(comment_pattern, __line) != None


def count_file_lines(__file_path: str):
    c = 0
    with open(__file_path) as f:
        for line in f:
            # Don't count blank lines
            c += not line.isspace() and not is_comment(line)
    return c


def get_runtime(__file_path: str):
    # print(__file_path.parts[-1])
    spec = importlib.util.spec_from_file_location(
        f"{__file_path.parts[-2]}.{__file_path.parts[-1]}", __file_path
    )
    mod = importlib.util.module_from_spec(spec)
    start_time = time.time()
    return round((time.time() - start_time) * 1000, 5)


def collect_imports(__file_path: str):
    imports = []
    with open(__file_path) as f:
        for line in f:
            # Pattern from: https://stackoverflow.com/a/53635205
            if (
                x := re.search(r"^\s*(?:from|import)\s+(\w+(?:\s*,\s*\w+)*)", line)
            ) != None:
                # group(1) extracts the library name. god-bless python regex.
                imports.append(x.group(1))
    return imports


def get_profiles(__file_path_list: list[Path]):
    profiles = []
    for file in __file_path_list:
        profiles.append(
            PythonFileProfile(
                _file_py=file.parts[-1],
                _parent_dir=file.parts[-2],
                _lines=count_file_lines(file),
                _process_time_ms=get_runtime(file),
                _imports=collect_imports(file),
                _full_file_path=file,
            )
        )
    return profiles


def build_profile_table(__grouped_profiles: list[PythonFileProfile]):
    data = ["File", "Lines", "Process Time", "Imports"]
    cols = len(data)
    rows = 1
    md_table = MdUtils("")
    for group, profiles in __grouped_profiles:
        data.extend([group] + (["-"] * (cols - 1)))
        rows += 1
        for profile in list(profiles):
            file_link = os.path.relpath(profile._full_file_path, working_dir).replace(
                "\\", "/"
            )
            data.extend(
                [
                    f"[{profile._file_py}]({file_link})",
                    profile._lines,
                    profile._process_time_ms,
                    ",".join(profile._imports),
                ]
            )
            rows += 1
    md_table.new_table(columns=4, rows=rows, text=data, text_align="center")
    return md_table.get_md_text()


def append_table(__table: str):
    with open("README.md", "r") as f:
        lines = f.readlines()
    table_start = lines.index("<!--TABLEBEGIN-->\n")
    table_end = lines.index("<!--TABLEEND-->\n")
    pre = "".join(lines[: table_start + 1])
    post = "".join(lines[table_end:])
    new = pre + __table + post
    with open("README.md", "w") as f:
        f.write(new)
    return


def main():
    # Remove profiler from the profiler.
    all_python_file_list = list(
        filter(lambda x: x != profiler_path, working_dir.rglob("*.py"))
    )

    profiles = get_profiles(all_python_file_list)
    grouped_profiles = itertools.groupby(profiles, lambda x: x._parent_dir)

    unpacked_groups = []
    for group, profiles in grouped_profiles:
        unpacked_groups.append(
            (group, sorted([x for x in profiles], key=lambda x: x._file_py))
        )

    sorted_profiles = sorted(unpacked_groups, key=lambda x: x[0])
    table = build_profile_table(sorted_profiles)
    append_table(table)


if __name__ == "__main__":
    main()
