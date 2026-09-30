from urllib.parse import urlsplit,urljoin
from typing import TypedDict 

def normalize_url(input_url: str)->str:

    parsed_url = urlsplit(input_url)
    full_path = f"{parsed_url.netloc}{parsed_url.path}"
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
