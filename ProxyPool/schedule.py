import logging
import time
from multiprocessing import Process
from ProxyPool.db import RedisClient
from ProxyPool.getter import FreeProxyGetter
from ProxyPool.settings import VALID_CHECK_CYCLE, POOL_LEN_CHECK_CYCLE, POOL_UPPER_THRESHOLD, POOL_LOWER_THRESHOLD
from ProxyPool.test import ValidityTester

logging.basicConfig(
        level=logging.INFO,
        filemode='a',
        format='%(asctime)s %(funcName)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'
    )


class ProxyPoolAdder(object):
    def __init__(self, threshold):
        self._conn = RedisClient()
        self._crawl = FreeProxyGetter()
        self._tester = ValidityTester()
        self._threshold = threshold
        self.logger = logging.getLogger(__name__)

    def is_full(self):
        """
        judge full
        """
        if self._conn.zset_len >= self._threshold:
            return False
        else:
            return True

    def add_to_zset(self):
        print('PoolAdder is working')
        proxy_count = 0
        while self.is_full():
            for i in range(self._crawl.__CrawlFuncCount__):
                callback = self._crawl.__CrawlFunc__[i]
                if callback != "crawl_quanwang":
                    raw_proxies = self._crawl.get_raw_proxies(callback)
                else:
                    raw_proxies = self._crawl.crawl_quanwang()
                self._tester.set_raw_proxies(raw_proxies)
                self._tester.test()
                proxy_count += len(raw_proxies)
                if not self.is_full():
                    self.logger.info("ip is enough")
                    break
            if proxy_count == 0:
                self.logger.error("unable to get IP")


class Schedule(object):
    @staticmethod
    def valid_proxies(cycle=VALID_CHECK_CYCLE):
        conn = RedisClient()
        tester = ValidityTester()
        while True:
            print("check valid proxies")
            count = int(conn.zset_len/2)
            if count == 0:
                print("add new valid proxies")
                time.sleep(cycle)
                continue
            proxies = conn.get(count)
            tester.set_raw_proxies(proxies)
            tester.test()
            time.sleep(cycle)

    @staticmethod
    def check_pool(cycle=POOL_LEN_CHECK_CYCLE, min=POOL_LOWER_THRESHOLD, max=POOL_UPPER_THRESHOLD):
        conn = RedisClient()
        adder = ProxyPoolAdder(max)
        while True:
            if conn.zset_len <= min:
                adder.add_to_zset()
            time.sleep(cycle)

    def run(self):
        print('Ip processing running')
        RedisClient().flush()
        valid_process = Process(target=Schedule.valid_proxies)
        check_process = Process(target=Schedule.check_pool)
        valid_process.start()
        check_process.start()
