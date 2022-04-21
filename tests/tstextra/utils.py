import logging
import boto3
import base64
import json
import os
import re
import sys
from pathlib import Path, PurePath
from botocore.exceptions import ClientError
from requests.auth import HTTPBasicAuth

LOG = logging.getLogger(__name__)

class SecretsManagerException(Exception):
    pass


def get_secret(secret_name, region_name="us-east-1", profile_name="default"):
    """Get secret value from Amazon SecretsManager.

    :param secret_name:
    :param region_name:
    """
    session = boto3.session.Session(profile_name="hgraph-np", region_name=region_name)
    client = session.client(service_name="secretsmanager", region_name=region_name)
    # In this sample we only handle the specific exceptions for the 'GetSecretValue' API.
    # See https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
    # We rethrow the exception by default.
    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        if "SecretString" in get_secret_value_response:
            LOG.info("Plaintext response from ASM")
            secret = get_secret_value_response["SecretString"]
            secret_dict = json.loads(secret)
            return secret_dict
        else:
            LOG.info("Binary response from ASM")
            decoded_binary_secret = base64.b64decode(
                get_secret_value_response["SecretBinary"]
            )
            return decoded_binary_secret
    except ClientError as e:
        error_code_str = (
            e.response["Error"]["Code"]
            if ("Error" in e.response and "Code" in e.response["Error"])
            else "no code/msg"
        )

        if error_code_str == "DecryptionFailureException":
            # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
            raise SecretsManagerException(
                "Could not decrypt secret text from ASM"
            ) from e
        elif error_code_str == "InternalServiceErrorException":
            # An error occurred on the server side.
            raise SecretsManagerException("Problem from ASM server") from e
        elif error_code_str == "InvalidParameterException":
            # You provided an invalid value for a parameter.
            raise SecretsManagerException("Invalid name or region given") from e
        elif error_code_str == "InvalidRequestException":
            # You provided a parameter value that is not valid for the current state of the resource.
            raise SecretsManagerException(
                "Resource could not be accessed with given params"
            ) from e
        elif error_code_str == "ResourceNotFoundException":
            # We can't find the resource that you asked for.
            raise SecretsManagerException(
                f"No secret with name '{secret_name}' and/or region '{region_name}'"
            ) from e
        else:
            raise SecretsManagerException(f"Unknown error: '{error_code_str}'") from e
    except Exception as e:
        raise e
    
def configure_service_auth():
    print(sys.path)
    # global API_AUTH
    if "PYTEST_CURRENT_TEST" in os.environ:
        from utils import get_secret

        logins = get_secret(
            "dev/h/platform/hgraph/datadelivery/access/read-write/authlist",
            profile_name="hgraph_np",
        )
        print(f"Using service account user: {logins[0]['user']}")
        api_auth = HTTPBasicAuth(logins[0]["user"], logins[0]["pass"])
    else:
        user = os.environ["API_USERNAME"]
        passwd = os.environ["API_PASSWORD"]
        api_auth = HTTPBasicAuth(user, passwd)
        print(api_auth)
    return api_auth

def find_git_rootdir():
    path = Path(os.path.dirname(__file__))
    entries = []
    fsroot = PurePath("/")
    while (path.parent != fsroot and not len(entries)):
        entries = [entry for entry in path.glob(".git")]
        path = path.parent
    return entries[0].parent if len(entries) > 0 else None

if __name__ == "__main__":
    s = get_secret("dev/h/platform/hgraph/datadelivery/access/read-write/authlist", profile_name="hgraph_np")
    print(s)
    
    repo_root_dir = find_git_rootdir()
    print(repo_root_dir)
