import requests
from collections import namedtuple
from requests.auth import AuthBase

TIER = "dev"
TestConfig = None

env_config_map = {}

def setup_module(module):
    """See: https://docs.pytest.org/en/7.0.x/how-to/xunit_setup.html"""
    global TestConfig
    # see: https://realpython.com/python-namedtuple/
    TestConfig = namedtuple("TestConfig", "baseurl httpauth")
    env_config_map["dev"] = TestConfig(
        "https://wp-dev.np.graph.hmelsevier.com",
        WPAuth("fc9fb3f2-3493-40c9-9ba6-dae2de171937"),
    )
    env_config_map["local"] = TestConfig(
        "https://127.0.0.1:8080/webprotege",
        WPAuth("5cec7c1f-6800-45b4-84de-f3de7616acb0"),
    )


def test_projects_list():
    url = f"{env_config_map[TIER].baseurl}/data/projects"
    auth = env_config_map[TIER].httpauth
    
    response = requests.get(url, auth=auth)
    projects = response.json()
    assert projects != None
    assert len(projects) > 0
    for project in projects:
        print(f"{project['projectId']}: {project['displayName']}")


class WPAuth(AuthBase):
    def __init__(self, apikey):
        self.apikey = apikey

    def __eq__(self, other):
        return self.apikey == getattr(other, "apikey", None)

    def __ne__(self, other):
        return not self == other

    def __call__(self, r):
        r.headers["Authorization"] = f"ApiKey {self.apikey}"
        return r


if __name__ == "__main__":
    """Only used when debugging without pytest runner"""
    pass
    """
    setup_module(None)
    test_projects_list()
    """
