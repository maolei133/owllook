import asyncio,aiohttp,sys
sys.path.append("/opt/codes/owllook")

from aiohttp import ClientSession
from owllook.config import RULES
 
async def fetch_status(session: ClientSession, url: str) -> int:
    try:
        async with session.get(url, timeout=5) as result:
            return result.status
    except Exception as e:
         pass
 
async def main(url: str):
    async with aiohttp.ClientSession() as session:
        status = await fetch_status(session, url)
        if status:
            print(f'Status for {url} was {status}')
 
 
if __name__ == '__main__':
    urls = ["https://" + x for x in RULES.keys()]
    for url in urls:
        asyncio.get_event_loop().run_until_complete(main(url))