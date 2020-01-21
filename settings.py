import os

ENV = os.environ

KV_CONFIG = {
    "host": "localhost",
    "port": 3313,
    "user": ENV["KV_USER"],
    "password": ENV["KV_PASS"],
}
