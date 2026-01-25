"""
Pytest configuration for iterable tests.
Ensures tests can find fixtures regardless of where pytest is run from.
"""

import os
import sys
from pathlib import Path

import pytest

# Get the tests directory
TESTS_DIR = Path(__file__).parent.absolute()

# Get the project root (parent of tests directory)
PROJECT_ROOT = TESTS_DIR.parent

# Add project root to Python path to ensure local code is used
# This prevents importing from installed packages when running tests
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Change to tests directory so relative paths work
# This ensures 'fixtures/...' paths work correctly
if os.getcwd() != str(TESTS_DIR):
    os.chdir(TESTS_DIR)


@pytest.fixture(autouse=True, scope="session")
def ensure_testdata_dir():
    """Ensure testdata directory exists for all tests."""
    testdata_dir = TESTS_DIR / "testdata"
    testdata_dir.mkdir(exist_ok=True)
    return testdata_dir
