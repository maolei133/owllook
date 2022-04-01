#!/usr/bin/env python
"""
 Created by howie.hu at 2018/5/28.
"""
import asyncio,sys
sys.path.append("/opt/codes/owllook")

from aiocache.serializers import PickleSerializer
from bs4 import BeautifulSoup
from urllib.parse import parse_qs, urlparse

from owllook.fetcher.decorators import cached
from owllook.fetcher.function import get_random_user_agent
from owllook.fetcher.novels_factory.base_novels import BaseNovels


class CustomNovels(BaseNovels):

    def __init__(self):
        super(CustomNovels, self).__init__()

    async def data_extraction(self, html, site):
        """
        小说信息抓取函数
        :return:
        """
        try:
            # 2017.09.09 修改 更加全面地获取title && url
            try:
                title = html.select('a')[0].get_text()
                url = site.url + html.select('a')[0].get('href', None)
            except Exception as e:
                self.logger.exception(e)
                return None
            
            netloc = urlparse(url).netloc
            if not url or 'baidu' in url or 'baike.so.com' in url or netloc in self.black_domain:
                return None
            is_parse = 1 if netloc in self.rules.keys() else 0
            is_recommend = 1 if netloc in self.latest_rules.keys() else 0
            time = ''
            timestamp = 0
            return {'title': title, 'url': url.replace('index.html', '').replace('Index.html', ''), 'time': time,
                    'is_parse': is_parse,
                    'is_recommend': is_recommend,
                    'timestamp': timestamp,
                    'netloc': netloc}
        except Exception as e:
            self.logger.exception(e)
            return None


    async def data_get(self, novels_name, headers, val):
        url = val.url + val.search_name
        params = {val.param_name: novels_name, }
        html = await self.fetch_url(url=url, params=params, headers=headers)
        print(html)
        
        soup = BeautifulSoup(html, 'html5lib')
        result = soup.find(class_=val.class_name)
        # print(result)
        
        a = result.select_one(val.a_name)
        # print(a)        
        return await self.data_extraction(html=result, site=val)


    async def novels_search(self, novels_name):
        """
        小说搜索入口函数
        :return:
        """
        headers = {
            'User-Agent': await get_random_user_agent()
        }
        
        values = self.site.values()
        res = [await self.data_get(novels_name=novels_name,headers=headers,val=val) for val in values]    
        return res
        


# @cached(ttl=259200, key_from_attr='novels_name', serializer=PickleSerializer(), namespace="novels_name")
async def start(novels_name):
    """
    Start spider
    :return:
    """
    return await CustomNovels.start(novels_name)


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start('雪中悍刀行'))


if __name__ == '__main__':
    main()