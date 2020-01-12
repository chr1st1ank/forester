#!/usr/bin/python
"""List basic information for all subfolders in the given path.

TODO: Add usage info
"""
from collections import namedtuple
import os
from os.path import realpath, relpath
import stat
import sys
from typing import Dict

from forester.util import cut_to_length, format_number, format_timestamp


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

        collected_info[path] = TreeInfo(total_n_files, total_n_folders, max_m_time)

        return collected_info[path]

    collect_folder_info(folder_path)
    if verbose:
        sys.stdout.write(f"\rScanned {len(collected_info)} folders           ")
        print("\n")
    return collected_info


def _output(path, *info_fields, column_widths):
    line = f"{cut_to_length(path, column_widths[0]-1).ljust(column_widths[0]-1)}"
    line += "".join(
        f" {cut_to_length(f, column_widths[i+1]-1).rjust(column_widths[i+1]-1)}"
        for i, f in enumerate(info_fields)
    )
    print(line)


def print_tree_info(args):
    column_widths = (50, 15, 15, 20)

    path = realpath(args.path)

    collected_info: Dict[str, TreeInfo] = tree_info(path, verbose=(not args.quiet))

    _output("Folder", "# Folders", "# Files", "m_time", column_widths=column_widths)
    print("-" * sum(column_widths))

    folders = sorted(
        filter(lambda k: realpath(k) != path, collected_info.keys()), reverse=True
    )
    folders.append(path)

    for f in folders:
        if f == path:
            print("=" * sum(column_widths))
        relative_to_target = relpath(f, path)
        if (  # Make sure we only print down to the desired max_depth
            args.max_depth is None
            or (relative_to_target.count(os.path.sep) < args.max_depth)
            or (f == path)  # Always keep root
        ):
            _output(
                relative_to_target,
                format_number(collected_info[f].folder_count),
                format_number(collected_info[f].file_count),
                format_timestamp(collected_info[f].last_mtime),
                column_widths=column_widths,
            )
