import os
import shlex
import subprocess
from contextlib import contextmanager
from typing import List

# logging.basicConfig(level=logging.DEBUG)


@contextmanager
def inside_dir(dirpath):
    """
    Execute code from inside the given directory
    :param dirpath: String, path of the directory the command is being run.
    """
    old_path = os.getcwd()
    try:
        os.chdir(dirpath)
        yield
    finally:
        os.chdir(old_path)


def run_inside_dir(commands, dirpath):
    """
    Run a command from inside a given directory, returning the exit status
    :param commands: Commands that will be executed
    :param dirpath: String, path of the directory the command is being run.
    """
    with inside_dir(dirpath):
        for command in commands:
            subprocess.check_call(shlex.split(command))


def check_output_inside_dir(command, dirpath):
    """Run a command from inside a given directory, returning the command output"""
    with inside_dir(dirpath):
        return subprocess.check_output(shlex.split(command))


def test_bake_with_defaults(cookies):
    result = cookies.bake()
    result_dir = result.project_path
    assert result_dir.is_dir()
    assert result.exit_code == 0
    assert result.exception is None

    found_toplevel_files = [f.name for f in result_dir.iterdir()]
    assert "pyproject.toml" in found_toplevel_files
    assert "tox.ini" in found_toplevel_files
    assert "tests" in found_toplevel_files

    # test that pre-commit runs without error for the generated project
    run_inside_dir(["git init"], result_dir)
    run_inside_dir(["pre-commit run --all-files"], result_dir)
