from pydoc import pager
import sys
from crawl import get_html,crawl_page
from crawl import  AsyncCrawler, crawl_site_async, write_json_report
import json
from urllib.parse import urlparse
import asyncio
ASYNC = True
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
   
    page_data = crawl_page(BASE_URL)    
    # with open('page_data.txt', 'w', encoding='utf-8') as f:
    #     json.dump(page_data, f, indent=4, ensure_ascii=False)
    fname = f"report.json"
    write_json_report(page_data,fname)

    
    print("DONE! bONA CIcCiO!")

async def main_async():
    print("Hello from web-scaper-py!")

    args = sys.argv
    if len(args)<2:
        print("no website provided")
        sys.exit(1)
    if len(args)>4:
        print("too many arguments provided")
        sys.exit(1)
    BASE_URL=args[1]
    MAX_CONCURRENCY = int(args[2])
    MAX_PAGES = int(args[3])
    string = f"MC{MAX_CONCURRENCY}_MP{MAX_PAGES}"
    
    print(f"starting crawl of: {BASE_URL}")
    #ASYNCHRONOUS VERSION
    
    page_data = await crawl_site_async(base_url=BASE_URL, max_concurrency=MAX_CONCURRENCY, max_pages=MAX_PAGES)
    write_json_report(page_data)
    with open(f'page_data_async_{string}.txt', 'w', encoding='utf-8') as f:
        json.dump(page_data, f, indent=4, ensure_ascii=False)
    for page in page_data.values():
        print(f"Found {len(page['outgoing_links'])} outgoing links on {page['url']}")
    print("DONE! bONA CIcCiO!")
    # print(page_data)


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
