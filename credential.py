import os
from os.path import join, dirname
from dotenv import load_dotenv

load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

URL = os.environ.get("URL")
SUCCESS_URL = os.environ.get("SUCCESS_URL")
ID = os.environ.get("ID")
PASS = os.environ.get("PASS")
Token = os.environ.get("TOKEN")
CHANNEL_ACCESS_TOKEN = os.environ.get("CHANNEL_ACCESS_TOKEN")
CHENNEL_SECRET = os.environ.get("CHENNEL_SECRET")
UID = os.environ.get("UID")
