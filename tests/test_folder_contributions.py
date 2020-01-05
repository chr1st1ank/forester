"""Unit tests for forester.folder_contributions"""
import os
import subprocess

import pytest

from forester import folder_contributions


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


def get_total_from_du(folder_name):
    """Get the size in bytes of a folder from the unix tool `du`"""
    du = subprocess.check_output(["du", "-bs", str(folder_name)])
    return int(du.split(b"\t")[0])


def test_total_size(folder_tree):
    """Teset if the total sizes from folder_contributions() are correct"""
    totals, _ = folder_contributions.folder_contributions(folder_tree, verbose=False)

    for f in ["d1", "d2"]:
        assert totals[f] == get_total_from_du(
            folder_tree / f
        ), f"Wrong total size for {f}"

    assert totals["."] == get_total_from_du(
        folder_tree
    ), f"Wrong total size for base folder"


def test_contribs(folder_tree):
    """Test if the contribution sizes from folder_contributions() are correct"""
    _, contribs = folder_contributions.folder_contributions(folder_tree, verbose=False)

    assert (
        contribs["d1"] == get_total_from_du(folder_tree / "d1") - 1024
    ), f"Wrong contrib size for d1"
    assert (
        contribs["d2"] == get_total_from_du(folder_tree / "d2") - 1024
    ), f"Wrong contrib size for d2"

    base_folder_size = (
        get_total_from_du(folder_tree)
        - get_total_from_du(folder_tree / "d1")
        - contribs["d2"]
    )
    assert contribs["."] == base_folder_size, f"Wrong contrib size for base folder"
