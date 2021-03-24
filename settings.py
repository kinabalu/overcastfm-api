import os
from dotenv import load_dotenv, find_dotenv, set_key
load_dotenv()

OVERCAST_COOKIE = os.getenv("OVERCAST_COOKIE")


def update_key(key, value):
    dotenv_file = find_dotenv()
    set_key(dotenv_file, key, value)
