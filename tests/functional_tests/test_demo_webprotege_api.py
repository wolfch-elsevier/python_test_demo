import os
import sys
from collections import namedtuple
import tests # __init__.py calls dotenv.dotenv_values to load the appropriate .env.* file

import requests

from tests.tstextra.utils import WPAuth

wp_auth = None
wp_base_url = None

def setup_module(module):
    """See: https://docs.pytest.org/en/7.0.x/how-to/xunit_setup.html"""
    global wp_auth, wp_base_url
    wp_auth = WPAuth(tests.config["WP_API_KEY"])
    wp_base_url = tests.config["WP_BASE_URL"]


def test_projects_list():
    url = f"{wp_base_url}/data/projects"
    
    response = requests.get(url, auth=wp_auth)
    projects = response.json()
    assert projects is not None
    assert len(projects) > 0
    for project in projects:
        print(f"{project['projectId']}: {project['displayName']}")


def test_unrecorded_hgraph_changes():
    url = f"{wp_base_url}/mongodb/webprotege/unrecorded_hgraph_changes/retrievals"
   
    filter = {
        "rev_status": "missing_id_field",
        "unrecorded_revision": {"user_id": "dd_test"},
    }
    params = {"filter": filter}
    response = requests.get(url, auth=wp_auth)
    assert response is not None
    print(response)


if __name__ == "__main__":
    """Only used when debugging without pytest runner"""
    print("hello")
    setup_module(None)
    # test_projects_list()
    test_unrecorded_hgraph_changes()
