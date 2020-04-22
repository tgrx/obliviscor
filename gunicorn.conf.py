"""
Config file for Gunicorn

For details, see:
https://devcenter.heroku.com/articles/python-gunicorn

Gunicorn max requests:
http://docs.gunicorn.org/en/latest/settings.html#max-requests

Gunicorn timeout:
# http://docs.gunicorn.org/en/latest/settings.html#timeout

"""
import multiprocessing
from os import getenv
from pathlib import Path

from dynaconf import settings

_here = Path(__file__).parent.resolve()
assert _here.is_dir(), f"invalid here dir: `{_here!r}`"

_port = getenv("PORT")
assert _port and _port.isdecimal(), f"invalid port: `{_port!r}`"
_port = int(_port)

_src_dir = (_here / "src").resolve()

bind = f"0.0.0.0:{_port}"
chdir = _src_dir.as_posix()
graceful_timeout = 10
max_requests = 200
max_requests_jitter = 20
pythonpath = _src_dir.as_posix()
reload = True
timeout = 30
workers = multiprocessing.cpu_count() * 2 + 1  # XXX hahaha classic

if settings.ENV_FOR_DYNACONF == "heroku":
    reload = False
    workers = int(getenv("WEB_CONCURRENCY", "4"))
