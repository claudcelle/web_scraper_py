from curses import echo
from email.mime import base
from operator import add
from urllib.parse import urlsplit,urljoin
from typing import TypedDict 
from types import TracebackType


def normalize_url(input_url: str|None)->str:

    parsed_url = urlsplit(input_url)
    if not parsed_url.scheme:
        full_path = f"{parsed_url.netloc}{parsed_url.path}"
    else:
        full_path = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
    full_path = full_path.rstrip("/")
    return full_path.lower()

    # parsed = urlsplit(input_url)
    # hostname = parsed.hostname
    # path = parsed.path

    # if hostname is None:
    #     if path == "":
    #         return ""
    #     if path.endswith("/"):
    #         path = path[:-1]
    #     if path.startswith("/"):
    #         path = path[1:]
    #     if path.startswith("www."):
    #         return path
    #     else:
    #         return f"www.{path}"

    # if hostname.startswith("www."):
    #     hostname = hostname[4:]

    # if path:
    #     if path == "/":
    #         return f"www.{hostname}"
    #     if path.endswith("/"):
    #         path = path[:-1]


    #     if path.startswith("/"):
    #         return f"www.{hostname}{path}"

    #     return f"www.{hostname}/{path}"
    # return f"www.{hostname}"


from bs4 import BeautifulSoup, Tag

def get_heading_from_html(html: str) -> str:
    soup = BeautifulSoup(html, 'html.parser')
    h_tag = soup.find('h1') or soup.find('h2')
    return h_tag.get_text(strip=True) if isinstance(h_tag, Tag) else ""

    # if h_tag:
    #     return h_tag.get_text(strip=True) if isinstance(h_tag, Tag) else ""
    # h_tag = soup.find('h2')
    # if h_tag:
    #     return h_tag.get_text(strip=True) if isinstance(h_tag, Tag) else ""
    # return ""


def get_first_paragraph_from_html(html: str) -> str:
    soup = BeautifulSoup(html, 'html.parser')
    main_tag = soup.find('main')
    if isinstance(main_tag,Tag):
        p_tag = main_tag.find('p')
        if isinstance(p_tag, Tag):
            return p_tag.get_text(strip=True)  
    
    h = soup.find('p')
    return  h.get_text(strip=True) if isinstance(h, Tag) else ""

def safe_urljoin(x,y):
    try:
        z = urljoin(x,y)
    except Exception as e:
        print(e)
    return z


def get_urls_from_html(html:str, base_url:str)->list[str]:
    soup = BeautifulSoup(html,'html.parser')
    urls = []
    anchors = soup.find_all('a')

    for a in anchors:
        if not isinstance(a,Tag):
            continue
        href = a.get('href')
        try:
            abs_url = urljoin(base_url, href)
            urls.append(abs_url)
        except Exception as e:
            print(f"{str(e)}: {href}")
    return urls


def get_images_from_html(html:str, base_url:str)->list[str]:
    soup = BeautifulSoup(html,'html.parser')
    urls = []
    images = soup.find_all('img')

    for a in images:
        if not isinstance(a,Tag):
            continue
        src = a.get('src')
        try:
            abs_url = urljoin(base_url, src)
            urls.append(abs_url)
        except Exception as e:
            print(f"{str(e)}: {src}")
    return urls
    # soup = BeautifulSoup(body, "html.parser")
    # return (
    #     list(map(
    #         lambda x: urljoin(url,x),
    #         list(
    #             map(
    #                 lambda x: x.get('src'),
    #                 soup.find_all('img')
    #                 )
    #             )
    #         )
    #     )
    # )


class PageData(TypedDict):
    url: str
    heading: str
    first_paragraph: str
    outgoing_links: list[str]
    image_urls: list[str]

def extract_page_data(html:str, page_url:str)->PageData:
    res: PageData = {
        "url" : page_url, 
        "heading": get_heading_from_html(html), 
        "first_paragraph": get_first_paragraph_from_html(html), 
        "outgoing_links": get_urls_from_html(html,page_url), 
        "image_urls": get_images_from_html(html,page_url)
    }
    return res

import requests
def get_html(url:str):
    try:
        resp = requests.get(url,headers={"User-Agent": "BootCrawler/1.0"})
    except Exception as e:
        print(f"Network Error while fetching {url}: {e}")

    if code := resp.status_code >= 400:
        raise Exception(f" HTTP status code {code}: {resp.reason}")
    
    content_type = resp.headers.get("content-type", "")
    if "text/html" not in content_type:
        raise Exception(f"got non-HTML response: {content_type}")
    

    return resp.text
    
from urllib.parse import urlparse
import logging
import sys

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)s | %(message)s",    
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)


def crawl_page(base_url, current_url=None, page_data=None):
    if not page_data:
        page_data = {}

    if not current_url:
        current_url = base_url

    if urlparse(base_url).netloc != urlparse(current_url).netloc:
        logger.debug("Exiting: base_url.netloc != current_url.netloc")
        logger.debug(
            "%s != %s",
            urlparse(base_url).netloc,
            urlparse(current_url).netloc
        )
        return

    current_url = normalize_url(current_url)

    if current_url in page_data:
        logger.debug("Exiting: current_url already in page_data: %s", current_url)
        return

    try:
        current_html = get_html(current_url)

        logger.info("Crawling: %s", current_url)

        current_data = extract_page_data(current_html, current_url)
        page_data[current_url] = current_data

        links = get_urls_from_html(current_html, current_url)

        for link in links:
            crawl_page(base_url, link, page_data)

    except Exception:
        logger.exception("Error while crawling %s", current_url)

    return page_data

import aiohttp
import asyncio
class AsyncCrawler:
    def __init__(self,base_url,max_concurrency = 10, max_pages = 100) -> None:
        self.base_url = base_url #(the starting URL)
        self.base_domain = urlparse(base_url).netloc #(the domain name)
        self.page_data: dict[str, PageData] = {} #(our dictionary of page data, keyed by normalized URL)
        self.visited: set[str] = set() #(a set of normalized URLs already scheduled for crawling)
        self.lock = asyncio.Lock() #(an asyncio.Lock to safely update page_data)
        self.semaphore = asyncio.Semaphore(max_concurrency) #(an asyncio.Semaphore - pass it the value of max_concurrency)
        self.session: aiohttp.ClientSession | None = None #(an aiohttp.ClientSession for making HTTP requests)
        self.max_pages = max_pages
        self.should_stop = False
        self.active_tasks = set()



    async def __aenter__(self)-> "AsyncCrawler":
        self.session = aiohttp.ClientSession()
        return self


    async def __aexit__(self, 
                        exc_type: type[BaseException] | None, 
                        exc_val: BaseException | None, 
                        exc_tb: TracebackType | None, 
                        ) -> None:
        if self.session is not None:
            await self.session.close()

    async def add_page_visit(self, normalized_url):
        if self.should_stop:
            return False
        if len(self.visited) >= self.max_pages:
            self.should_stop = True
            print("Reached maximum number of pages to crawl.")
            return False
        async with self.lock:
            if normalized_url in self.visited:
                return False
            self.visited.add(normalized_url)
            return True
        
    async def get_html(self, url:str):
        if self.session is None:
            return None
        try:
            async with self.session.get( 
                url, 
                headers={"User-Agent": "BootCrawler/1.0"}
                ) as resp:
                code = resp.status
                if code >= 400:
                    logger.warning(f" HTTP status code {code}: {resp.reason}")
                content_type = resp.content_type
                if "text/html" not in content_type:
                    logger.warning(f"got non-HTML response: {content_type}")
                text = await resp.text()
                return text 
        except Exception as e:
            print(f"Network Error while fetching {url}: {e}")
            return None

    async def crawl_page(self, current_url=None):

        if not current_url:
            current_url = self.base_url

        try:
            if urlparse(self.base_url).netloc != urlparse(current_url).netloc:
                logger.debug("Exiting: base_url.netloc != current_url.netloc")
                logger.debug(
                    "%s != %s",
                    urlparse(self.base_url).netloc,
                    urlparse(current_url).netloc
                )
                return
        
            if not await self.add_page_visit(normalize_url(current_url)):
                return self.page_data

            current_url = normalize_url(current_url)

            if current_url in self.page_data:
                logger.debug("Exiting: current_url already in page_data: %s", current_url)
                return

            async with self.semaphore:
                current_html = await self.get_html(current_url)
            if current_html is None:
                logger.warning(f"Failed to get HTML for {current_url}")
                return
            logger.info("Crawling: %s", current_url)

            current_data = extract_page_data(current_html, current_url)
            async with self.lock:
                self.page_data[current_url] = current_data

            # links = get_urls_from_html(current_html, current_url)
            links = current_data["outgoing_links"]

            tasks = []
            for link in links:
                task = asyncio.create_task(self.crawl_page(link))
                tasks.append(task)
                self.active_tasks.add(task)

            await asyncio.gather(*tasks)
                    

        except Exception as e :
            logger.exception("Error while crawling %s: %s", current_url, e)
            return None
        finally:
            self.active_tasks.remove(asyncio.current_task())

        return self.page_data
    async def crawl(self):
        if self.should_stop:
            return self.page_data
        task = asyncio.create_task(self.crawl_page(self.base_url))
        self.active_tasks.add(task)
        await task
        return self.page_data
async def crawl_site_async(base_url, max_concurrency, max_pages):
    async with AsyncCrawler(base_url, max_concurrency, max_pages) as crawler:
        return await crawler.crawl()
