from dataclasses import dataclass
from time import *
import re
from mdutils.mdutils import MdUtils
import itertools


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


def is_comment(__line: str):
    return re.match(comment_pattern, __line) != None


def count_file_lines(__file_path: str):
    c = 0
    with open(__file_path) as f:
        for line in f:
            # Don't count blank lines
            c += not line.isspace() and not is_comment(line)
    return c


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
                _process_time_ms=None,
                _imports=collect_imports(file),
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
            data.extend(
                [
                    profile._file_py,
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
    table = build_profile_table(grouped_profiles)
    append_table(table)


if __name__ == "__main__":
    main()
