import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

USERS_PROD_PORT = os.environ.get("USERS_PROD_PORT")
USERS_TEST_PORT = os.environ.get("USERS_TEST_PORT")
FREE_PROVIDER_PORT = os.environ.get("FREE_PROVIDER_PORT")
PAID_PROVEDER_PORT = os.environ.get("PAID_PROVEDER_PORT")
AUTH_SECRET = os.environ.get("AUTH_SECRET")
