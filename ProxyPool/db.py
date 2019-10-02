import logging
import redis
from ProxyPool.settings import HOST, PORT, PASSWORD

logging.basicConfig(
        level=logging.INFO,
        filename='./logger.log',
        filemode='a',
        format='%(asctime)s %(funcName)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'
    )


class RedisClient(object):
    """
    redis database operations
    """
    def __init__(self, host=HOST, port=PORT):
        self.logger = logging.getLogger(__name__)
        if PASSWORD:
            self._db = redis.Redis(host=host, port=port, password=PASSWORD)
        else:
            self._db = redis.Redis(host=host, port=port)

    def get(self, count=1):
        """
        get proxies from zset,mainly used for inspections
        """
        if count > self._db.zcard("proxies"):
            self.logger.error("Exceed maximum")
            return
        proxies = self._db.zrevrange("proxies", start=-count, end=-1)
        self._db.zremrangebyrank("proxies", 0, count-1)
        return [proxy.decode("utf-8") for proxy in proxies]

    def add(self, proxy):
        """
        add proxy to zset
        """
        scores_max = self._db.zrevrange("proxies", 0, 0, withscores=True)
        if not scores_max:
            self._db.zadd("proxies", {proxy: 0})
        else:
            self._db.zadd("proxies", {proxy: scores_max[0][1]+2})

    def flush(self):
        """
        flush db
        """
        self._db.flushall()

    def pop(self):
        recent = self._db.zrevrange("proxies", start=0, end=0)[0].decode('utf-8')
        self._db.zremrangebyrank("proxies", -1, -1)
        return recent

    @property
    def zset_len(self):
        """
        get length from zset.
        """
        return self._db.zcard("proxies")


if __name__ == '__main__':
    r = RedisClient()
    # r.add('127.7.7.1:89 ')
    print(r.get(2))
    pass
