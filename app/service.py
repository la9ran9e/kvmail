import logging
from tarantool import Connection
from tarantool.error import DatabaseError


logger = logging.getLogger(__name__)


class KV:
    def __init__(self, *, host, port, user, password):
        self.space = "kv"
        self.conn = Connection(host, port,  user=user, password=password)

    def put(self, key, value):
        try:
            ret = self.conn.insert(self.space, (key, value))
        except DatabaseError as err:
            if err.args[0] == 3:
                logger.warning(f"Key {key!r} already exists")
                raise KeyError(f"Key {key!r} already exists")
            else:
                raise
        else:
            return ret.data

    def get(self, key):
        ret = self.conn.select(self.space, key)
        if not ret.data:
            logger.warning(f"Key {key!r} does not exist")
            raise KeyError(f"Key {key!r} does not exist")
        return ret.data[0][1]

    def update(self, key, updater):
        data = self.get(key)
        data.update(updater)
        # delete null's keys
        data = {k: v for k, v in data.items() if v is not None}
        ret = self.conn.update(self.space, key, [("=", 1, data)])
        return ret.data[0][1]

    def delete(self, key):
        ret = self.conn.delete(self.space, key)
        if not ret.data:
            logger.warning(f"Key {key!r} does not exist")
            raise KeyError(f"Key {key!r} does not exist")
        return ret.data[0][1]
