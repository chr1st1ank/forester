"""Unit tests for forester.tree_info"""
import os
from unittest.mock import patch
import re
import sys

import pytest

from forester import tree_info


@pytest.fixture
def folder_tree(tmp_path):
    """Create a folder tree with some links"""
    # Create empty folders
    d1 = tmp_path / "d1"
    d1.mkdir()

    d2 = tmp_path / "d2"
    d3 = d2 / "d3"
    d3.mkdir(parents=True)

    # Place some files in there
    # (tmp_path / "testfile").write_bytes(b'X' * 1024)
    (d1 / "testfile").write_bytes(b"X" * 1024)
    (d2 / "testfile").write_bytes(b"X" * 1024)
    (d3 / "symlink").symlink_to(d1 / "testfile")
    os.link(dst=str(d3 / "hardlink"), src=str(d1 / "testfile"))

    return tmp_path


@pytest.fixture()
def collected_info_and_path(folder_tree):
    return tree_info.tree_info(folder_tree), folder_tree


def test_tree_info_folder_count(collected_info_and_path):
    """Test if the number of folders shown is correct"""
    collected_info, tree_path = collected_info_and_path
    folder_counts = {path: i.folder_count for path, i in collected_info.items()}
    assert folder_counts[str(tree_path)] == 4


@pytest.mark.parametrize(
    "main_output_regex",
    [
        r"""^.*
Folder                                                 # Folders        # Files              m_time
----------------------------------------------------------------------------------------------------
d2/d3                                                          1              2 \d{4}-\d\d-\d\d \d\d:\d\d:\d\d
d2                                                             2              3 \d{4}-\d\d-\d\d \d\d:\d\d:\d\d
d1                                                             1              1 \d{4}-\d\d-\d\d \d\d:\d\d:\d\d
----------------------------------------------------------------------------------------------------
.                                                              4              4 \d{4}-\d\d-\d\d \d\d:\d\d:\d\d$"""
    ],
)
def test_tree_info_main(capsys, folder_tree, main_output_regex):
    with patch.object(sys, "argv", ["tree_info.py", str(folder_tree.absolute())]):
        tree_info.main()

    out, err = capsys.readouterr()
    print()
    print(out)
    print()

    assert not err
    assert re.match(
        main_output_regex, out, re.DOTALL
    ), f"Output string doesn't match regex: {out}"
