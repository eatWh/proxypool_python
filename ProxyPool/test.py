import asyncio
import logging
import aiohttp
from ProxyPool.db import RedisClient
from ProxyPool.settings import TEST_API

logging.basicConfig(
        level=logging.INFO,
        filename='./logger.log',
        filemode='a',
        format='%(asctime)s %(funcName)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'
    )


class ValidityTester(object):
    test_api = TEST_API

    def __init__(self):
        self._raw_proxies = None
        self._available_proxies = []
        self._conn = RedisClient()
        self.logger = logging.getLogger(__name__)

    def set_raw_proxies(self, proxies):
        self._raw_proxies = proxies

    async def test_one_proxy(self, proxy):
        async with aiohttp.ClientSession() as session:
            if isinstance(proxy, bytes):
                proxy = proxy.decode('utf-8')
            real_proxy = "http://" + proxy
            try:
                async with session.get(ValidityTester.test_api, proxy=real_proxy, timeout=10) as rep:
                    if rep.status == 200:
                        self._conn.add(proxy)
                        self.logger.info("valid proxy:"+proxy)
            except Exception as e:
                self.logger.error("invalid proxy:"+proxy)

    def test(self):
        """
        aio test all proxies.
        """
        print('ValidityTester is working')
        try:
            loop = asyncio.get_event_loop()
            tasks = [self.test_one_proxy(proxy) for proxy in self._raw_proxies]
            loop.run_until_complete(asyncio.wait(tasks))
        except ValueError:
            self.logger.error('Async Error')


if __name__ == '__main__':
    a = ValidityTester()
    a.set_raw_proxies(['134.175.135.224:80',
'207.180.226.111:80',
'173.197.169.6:8080',
'24.245.100.212:48678',
'70.169.28.194:48678',
'75.73.50.82:80',
'45.168.74.6:8080',
'75.151.213.85:8080',
'96.9.87.54:49242',
'157.55.201.215:80'])
    a.test()
    pass