import os

path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)
os.chdir(dir_path)

try:
    import waitress
except ImportError:
    os.system('pip3 install -r requirements.txt')

from api import api
from elk import connection as elk_conn
from reader.arg import ArgReader
from werkzeug.serving import run_with_reloader


db = ArgReader.read()

print(f'{db.config.title} version:{db.config.version}')

if db.version is not None:
    print(db.version)
else:
    elk_conn(endpoint=db.es_endpoint, timeout=db.es_timeout, retry_period=db.es_retry_period)

    @run_with_reloader
    def run_server():
        waitress.serve(api(title=db.config.title, version=db.config.version,
                           dev_username=db.dev_username, dev_password=db.dev_password),
                           host=db.host, port=db.port)

    run_server()
