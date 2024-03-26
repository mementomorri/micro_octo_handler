import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

AUTH_SECRET = os.environ.get("AUTH_SECRET")
TOKEN_LIFETIME = os.environ.get("TOKEN_LIFETIME")
TOKEN_ALGORITHM = os.environ.get("TOKEN_ALGORITHM")
