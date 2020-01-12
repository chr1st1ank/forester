"""Command line interface for all modules"""
import argparse
import os
import sys

import forester
from forester import folder_contributions, tree_info


def main(*raw_args):
    # Main parser
    parser = argparse.ArgumentParser(description="Swiss-army knife for directory trees")
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress unnecessary output, such as progress reports",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s version {forester.__version__}"
    )
    subparsers = parser.add_subparsers()

    # Parser for subcommand "info"
    info_parser = subparsers.add_parser(
        "info", help="Informative directory tree overview"
    )
    info_parser.add_argument(
        "--max-depth",
        type=int,
        help="Print the total for a directory only if it is N or fewer levels "
        "below the command line argument",
    )
    info_parser.add_argument(
        "path", default=os.getcwd(), nargs="?", help="Directory to analyze"
    )
    info_parser.set_defaults(func=tree_info.print_tree_info)

    # Parser for subcommand "contribs"
    contribs_parser = subparsers.add_parser(
        "contribs", help="List the contributions of subfolders to the total disk space",
    )
    contribs_parser.add_argument(
        "path", default=os.getcwd(), nargs="?", help="Directory to analyze"
    )
    contribs_parser.set_defaults(func=folder_contributions.print_folder_contributions)

    # Common path argument
    args = parser.parse_args(raw_args)

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_usage()


def call_main():
    main(*sys.argv[1:])


if __name__ == "__main__":
    call_main()
