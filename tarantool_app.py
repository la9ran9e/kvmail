import os
import sys
import shlex
import subprocess

from dotenv import load_dotenv

load_dotenv()
app = subprocess.Popen(shlex.split(f"{os.getenv('TARANTOOL_HOME')}/src/tarantool app.lua"), stdout=sys.stdout, stderr=sys.stderr)
app.wait()
