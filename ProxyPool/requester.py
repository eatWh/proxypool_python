from requests import get
from requests.exceptions import ConnectionError
import random
from ProxyPool.settings import USER_AGENT
import logging

logging.basicConfig(
        level=logging.INFO,
        filemode='a',
        format='%(asctime)s %(funcName)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'
    )


def get_html(url):
    logger = logging.getLogger(__name__)
    user_agent = random.choice(USER_AGENT)
    headers = {
        "user-agent": user_agent,
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9"
    }
    try:
        rep = get(url, headers=headers, timeout=30)
        if rep.status_code == 200:
            logger.info("Getting result：" + url)
            # rep.encoding = rep.apparent_encoding
            return rep.text
    except ConnectionError:
        logger.error("Crawling Failed", url)
        return None

# class Downloader(object):
#     """
#     异步下载器，可以对代理源异步抓取，但是容易被BAN。
#     """
#
#     def __init__(self, urls):
#         self.urls = urls
#         self._htmls = []
#
#     async def download_single_page(self, url):
#         async with aiohttp.ClientSession() as session:
#             async with session.get(url) as resp:
#                 self._htmls.append(await resp.text())
#
#     def download(self):
#         loop = asyncio.get_event_loop()
#         tasks = [self.download_single_page(url) for url in self.urls]
#         loop.run_until_complete(asyncio.wait(tasks))
#
#     @property
#     def htmls(self):
#         self.download()
#         return self._htmls
