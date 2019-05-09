import os
import records

from utils import get_config


class Database(object):
    def __init__(self):
        _config = get_config()

        self._env = os.environ.get('FLASK_ENV', default='development')

        self.db_url = "{}://{}:{}@{}:{}/{}".format(
            _config["db_credentials"][self._env]["driver"],
            _config["db_credentials"][self._env]["username"],
            _config["db_credentials"][self._env]["password"],
            _config["db_credentials"][self._env]["hostname"],
            _config["db_credentials"][self._env]["port"],
            _config["db_credentials"][self._env]["database"],
        )

    def __enter__(self):
        self.conn = records.Database(db_url=self.db_url)

        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()
