#!/usr/bin/python
"""List basic information for all subfolders in the given path.

TODO: Add usage info
"""
from collections import namedtuple
import os
import stat
import sys
from typing import Dict

from command.util import format_number


TreeInfo = namedtuple("TreeInfo", ["file_count", "folder_count", "last_mtime"])


def tree_info(folder_path, verbose=False) -> Dict[str, TreeInfo]:
    """Get the total disk space and disk space contributions of all subfolders in the given path.

    Returns:
        Dictionary: (totals, contributions)
        Both are in the form {folder_name: size}
    """
    folder_path = str(folder_path)
    collected_info = {}

    def collect_folder_info(path: str) -> TreeInfo:
        assert os.path.isdir(path)

        # Display progress info
        if verbose and len(collected_info) % 100 == 0:
            sys.stdout.write(f"\r... scanning ({len(collected_info)} folders) ...")
            sys.stdout.flush()

        # Collect data about the folder itself
        st = os.lstat(path)
        max_m_time = st[stat.ST_MTIME]
        total_n_files = 0
        total_n_folders = 1

        # Collect data about the children
        for dir_entry in os.scandir(path):
            if dir_entry.is_dir(follow_symlinks=False):
                n_files, n_folders, m_time = collect_folder_info(dir_entry.path)
                total_n_files += n_files
                total_n_folders += n_folders
                max_m_time = max(max_m_time, m_time)
            else:
                max_m_time = max(
                    max_m_time, dir_entry.stat(follow_symlinks=False)[stat.ST_MTIME]
                )
                total_n_files += 1

        collected_info[path] = TreeInfo(
            total_n_files, total_n_folders, max_m_time
        )

        return collected_info[path]

    collect_folder_info(folder_path)
    if verbose:
        print("\n")
    return collected_info


def _output(path: str, *info_fields, name_width, number_width):
    print(
        f"{path[-name_width:].ljust(name_width)}"
        + "".join(f"{format_number(f).rjust(number_width)}" for f in info_fields)
    )


def main():
    name_width = 50
    number_width = 15

    p = sys.argv[1].strip()
    if p[-1] == os.path.sep and len(p) > 1:
        p = p[:-1]

    collected_info: Dict[str, TreeInfo] = tree_info(p, verbose=True)

    _output(
        "Folder",
        "# Folders",
        "# Files",
        "m_time",
        name_width=name_width,
        number_width=number_width,
    )
    print("-" * (name_width + 3 * number_width))

    folders = sorted(collected_info.keys(), reverse=True)

    for f in folders:
        _output(
            f,
            collected_info[f].folder_count,
            collected_info[f].file_count,
            collected_info[f].last_mtime,
            name_width=name_width,
            number_width=number_width,
        )

    print("-" * (name_width + 3 * number_width))
    _output(
        "Total",
        sum(i.folder_count for i in collected_info.values()),
        sum(i.file_count for i in collected_info.values()),
        max(i.last_mtime for i in collected_info.values()),
        name_width=name_width,
        number_width=number_width,
    )

if __name__ == "__main__":
    main()
