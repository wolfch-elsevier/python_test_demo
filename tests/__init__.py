import sys
from dotenv import dotenv_values
import os

# sys.stderr.write("************* Called __init__.py ***************\n")

runenv = os.environ.get("RUNENV", "dev")
if runenv == "dev":
    config = dotenv_values(".env.dev")
else:
    config = dotenv_values(".env.prod")

