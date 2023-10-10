from asyncio import Semaphore, gather, get_event_loop, run, ensure_future
from asyncio.exceptions import TimeoutError
from aiohttp import ClientSession
from requests import get

async def fetch(semaphore, session, url):
    try:
        async with semaphore, session.get(url, timeout=10) as response:
            return await response.text()
    except TimeoutError:
        return None
    except UnicodeDecodeError:
        return await response.text(encoding="ISO-8859-1")

async def fetch_all(urls, numSemaphore=600):
    semaphore = Semaphore(numSemaphore)
    tasks = []

    async with ClientSession() as session:
        for url in urls:
            tasks.append(ensure_future(fetch(semaphore, session, url)))
        
        return await gather(*tasks)

def get_html_from_urls(urls):
    return get_event_loop().run_until_complete(fetch_all(urls))
    
def get_html_from_url(url):
    return get(url).text