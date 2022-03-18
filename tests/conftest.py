"""
See: https://docs.pytest.org/en/6.2.x/fixture.html#conftest-py-sharing-fixtures-across-multiple-files
"""
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "tstextra"))
