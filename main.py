from pydoc import pager
import sys
from crawl import get_html,crawl_page
from crawl import  AsyncCrawler, crawl_site_async
import json
from urllib.parse import urlparse
import asyncio
ASYNC = False
def main():
    print("Hello from web-scaper-py!")

    args = sys.argv
    if len(args)<2:
        print("no website provided")
        sys.exit(1)
    if len(args)>2:
        print("too many arguments provided")
        sys.exit(1)
    BASE_URL=args[1]
    
    print(f"starting crawl of: {BASE_URL}")
       # SYNCHRONOUS VERSION
    # print(get_html(BASE_URL))
   
    page_data = crawl_page(BASE_URL)    
    with open('page_data.txt', 'w', encoding='utf-8') as f:
        json.dump(page_data, f, indent=4, ensure_ascii=False)

    
    print("DONE! bONA CIcCiO!")

async def main_async():
    print("Hello from web-scaper-py!")

    args = sys.argv
    if len(args)<2:
        print("no website provided")
        sys.exit(1)
    if len(args)>2:
        print("too many arguments provided")
        sys.exit(1)
    BASE_URL=args[1]
    
    print(f"starting crawl of: {BASE_URL}")
    #ASYNCHRONOUS VERSION
    
    page_data = await crawl_site_async(BASE_URL, urlparse(BASE_URL).netloc, 10)
    with open('page_data_aync.txt', 'w', encoding='utf-8') as f:
        json.dump(page_data, f, indent=4, ensure_ascii=False)

    print("DONE! bONA CIcCiO!")


import time

if __name__ == "__main__":
    start = time.perf_counter()

    if ASYNC:
        asyncio.run(main_async())
        v = 'Async'
    else:
        main()
        v='Sync'

    elapsed = time.perf_counter() - start
    print(f"Elapsed: {elapsed:.3f} seconds for {v}")
