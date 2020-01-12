"""Test the cli module to check the handling of command line arguments."""
from unittest import mock
import re
import pytest
import forester
from forester import cli


@pytest.fixture()
def ensure_no_action_calls():
    """Mock all action functions and ensure they raise an error if they are called."""
    with mock.patch(
        "forester.folder_contributions.print_folder_contributions"
    ) as mock_contrib, mock.patch("forester.tree_info.print_tree_info") as mock_info:
        mock_contrib.side_effect = RuntimeError(
            "print_folder_contributions was unexpectedly called!"
        )
        mock_info.side_effect = RuntimeError("print_tree_info was unexpectedly called!")

        yield


def test_version(ensure_no_action_calls, capsys):
    """Ensure the parameter `version` makes the cli print the current version number"""
    with pytest.raises(SystemExit) as exit_error:
        cli.main("--version")
    assert exit_error.value.code == 0, "Expected application to exit with code 0"
    out, err = capsys.readouterr()
    assert err == "", "Expected no output on stderr!"
    assert (
        f"version {forester.__version__}" in out
    ), "Version number not printed to stdout"


@pytest.mark.parametrize("params", [[], ["--quiet"]])
def test_usage(ensure_no_action_calls, capsys, params):
    """Ensure usage hint is shown on too few parameters."""
    cli.main(*params)
    out, err = capsys.readouterr()
    assert err == "", "Expected no output on stderr!"
    assert re.match(
        r"^usage: .+\.py \[\-h\] \[\-\-quiet\] \[\-\-version\] "
        r"\{info,contribs\} \.\.\.$",
        out,
    ), "No usage hint or in wrong format!"


@pytest.fixture()
def mock_tree_info():
    """Mock all action functions and ensure they raise an error if they are called."""
    with mock.patch(
        "forester.folder_contributions.print_folder_contributions"
    ) as mock_contrib, mock.patch("forester.tree_info.print_tree_info") as mock_info:
        mock_contrib.side_effect = RuntimeError(
            "print_folder_contributions was unexpectedly called!"
        )

        yield mock_info


@pytest.mark.parametrize(
    "cli_args, expected_args",
    [
        (("info",), ("path",)),
        (("info", "."), ("path",)),
        (("info", "--max-depth", "3", "."), ("path", "max_depth")),
    ],
)
def test_tree_info_params(mock_tree_info, cli_args, expected_args):
    """Ensure the right args get passed to `print_tree_info`"""
    cli.main(*cli_args)
    for a in expected_args:
        assert hasattr(mock_tree_info.call_args, a)


@pytest.fixture()
def mock_folder_contributions():
    """Mock all action functions and ensure they raise an error if they are called."""
    with mock.patch(
        "forester.folder_contributions.print_folder_contributions"
    ) as mock_contrib, mock.patch("forester.tree_info.print_tree_info") as mock_info:
        mock_info.side_effect = RuntimeError(
            "print_tree_info was unexpectedly called!"
        )

        yield mock_contrib


@pytest.mark.parametrize(
    "cli_args, expected_args",
    [
        (("contribs",), ("path",)),
        (("contribs", "."), ("path",)),
        (("contribs", "--max-depth", "3", "."), ("path", "max_depth")),
    ],
)
def test_folder_contrib_params(mock_folder_contributions, cli_args, expected_args):
    """Ensure the right args get passed to `print_tree_info`"""
    cli.main(*cli_args)
    for a in expected_args:
        assert hasattr(mock_folder_contributions.call_args, a)
