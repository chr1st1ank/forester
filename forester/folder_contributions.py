#!/usr/bin/python
"""List the total disk space and disk space contributions of all subfolders in the given path.

Both figures only differ if there are inodes which are hardlinks from multiple of these
folders. Then the contributions show how much disk space would be gained if one of the
folders would be deleted. Inodes with hardlinks from outside would not be deleted in
this case.
"""
import os
import stat
import sys

from forester.util import format_number


def folder_contributions(folder_path, verbose):
    """Get the total disk space and disk space contributions of all subfolders in the given path.

    Returns:
        Tuple of dictionaries: (totals, contributions)
        Both are in the form {folder_name: size}
    """
    folder_path = str(folder_path)
    inodes_read = set()
    inode_sizes = {}

    def getsize(folder_path, recurse=True):
        assert os.path.isdir(folder_path)

        if verbose and len(inode_sizes) % 100 == 0:
            sys.stdout.write(f"\r... scanning ({len(inode_sizes)} folders) ...")
            sys.stdout.flush()

        # Collect data about the folder itself
        st = os.lstat(folder_path)
        uniqueinode = "%s%s" % (st[stat.ST_INO], st[stat.ST_DEV])
        size = st[stat.ST_SIZE]
        inode_sizes[uniqueinode] = size
        inodes_read.add(uniqueinode)
        inodes = {uniqueinode}

        # Collect data about the children
        for dir_entry in os.scandir(folder_path):
            if dir_entry.is_dir(follow_symlinks=False):
                if recurse:
                    s, i = getsize(dir_entry.path)
                    size += s
                    inodes.update(i)
            else:
                uniqueinode = "%s%s" % (
                    dir_entry.inode(),
                    dir_entry.stat(follow_symlinks=False)[stat.ST_DEV],
                )
                inodes.add(uniqueinode)
                if uniqueinode in inodes_read:
                    size += inode_sizes[uniqueinode]
                else:
                    size += dir_entry.stat(follow_symlinks=False)[stat.ST_SIZE]
                    inode_sizes[uniqueinode] = dir_entry.stat(follow_symlinks=False)[
                        stat.ST_SIZE
                    ]
                    inodes_read.add(uniqueinode)

        return size, inodes

    def calc_contribution(inodes, inode_sets):
        exclusive_inodes = inodes
        for s in inode_sets:
            exclusive_inodes = exclusive_inodes.difference(s)

        return sum([inode_sizes[i] for i in exclusive_inodes])

    folder_names = [
        f
        for f in os.listdir(folder_path)
        if os.path.isdir(folder_path + "/" + f) and f != "."
    ]
    inode_sets = {}
    totals = {}
    for f in folder_names:
        s, i = getsize(folder_path + "/" + f)
        inode_sets[f] = i
        totals[f] = s

    if verbose:
        sys.stdout.write(f"\rScanned {len(inodes_read)} inodes                      \n")
        sys.stdout.flush()

    contributions = {}
    for f in folder_names:
        contributions[f] = calc_contribution(
            inode_sets[f], [inode_sets[other] for other in folder_names if other != f]
        )

    s, i = getsize(folder_path, recurse=False)
    totals["."] = sum(inode_sizes.values())
    contributions["."] = calc_contribution(i, inode_sets)

    return totals, contributions


def output(name, total, contrib, colsize):
    print(
        f"{name.ljust(colsize)}{format_number(total).rjust(colsize)}"
        f"{format_number(contrib).rjust(colsize)}"
    )


def print_folder_contributions(args):
    colsize = 30
    sort_order = "contribs"

    p = os.path.realpath(args.path)

    totals, contributions = folder_contributions(p, verbose=(not args.quiet))

    output("Folder", "Total size (B)", "Size of unique inodes (B)", colsize)
    print("-" * (3 * colsize))

    if sort_order == "name":
        folders = sorted(totals.keys(), reverse=True)
    elif sort_order == "totals":
        folders = (k for k, v in sorted(totals.items(), key=lambda item: item[1]))
    elif sort_order == "contribs":
        folders = (
            k for k, v in sorted(contributions.items(), key=lambda item: item[1])
        )

    for f in folders:
        if f != ".":
            output(f, totals[f], contributions[f], colsize)

    print("=" * (3 * colsize))
    output("Total", totals["."], "-", colsize)
