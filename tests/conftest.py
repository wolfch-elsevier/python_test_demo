"""
See: https://docs.pytest.org/en/6.2.x/fixture.html#conftest-py-sharing-fixtures-across-multiple-files
"""
import sys
import os
import pytest
from dotenv import dotenv_values

sys.path.append(os.path.join(os.path.dirname(__file__), "tstextra"))


