#!/usr/bin/env python

"""Tests for `poast` package."""

# import pytest
from click.testing import CliRunner
from poast.openapi3 import cli


def test_cli_help():
    """Test the CLI help menu."""
    runner = CliRunner()
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
