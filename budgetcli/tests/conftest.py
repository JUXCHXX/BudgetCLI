"""Pytest configuration and shared fixtures."""

import tempfile
from pathlib import Path

import pytest

from budgetcli.database import init_db


@pytest.fixture(scope="session")
def test_db_dir():
    """Create temporary directory for test databases."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def temp_db(test_db_dir):
    """Create temporary database for each test."""
    db_path = str(Path(test_db_dir) / f"test_{id(test_db_dir)}.db")
    init_db(db_path)
    yield db_path


@pytest.fixture
def temp_export_dir():
    """Create temporary export directory for each test."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir
