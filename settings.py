import os

from dotenv import load_dotenv


load_dotenv()


KV_CONFIG = {
    "host": "localhost",
    "port": 3313,
    "user": os.getenv("KV_USER"),
    "password": os.getenv("KV_PASS"),
}
