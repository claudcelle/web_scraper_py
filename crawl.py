from urllib.parse import urlsplit,urljoin
def normalize_url(input_url: str)->str:

    parsed = urlsplit(input_url)
    hostname = parsed.hostname
    path = parsed.path

    if hostname is None:
        if path == "":
            return ""
        if path.endswith("/"):
            path = path[:-1]
        if path.startswith("/"):
            path = path[1:]
        if path.startswith("www."):
            return path
        else:
            return f"www.{path}"

    if hostname.startswith("www."):
        hostname = hostname[4:]

    if path:
        if path == "/":
            return f"www.{hostname}"
        if path.endswith("/"):
            path = path[:-1]


        if path.startswith("/"):
            return f"www.{hostname}{path}"

        return f"www.{hostname}/{path}"
    return f"www.{hostname}"


from bs4 import BeautifulSoup, Tag

def get_heading_from_html(html: str) -> str:
    soup = BeautifulSoup(html, 'html.parser')
    h_tag = soup.find('h1')
    if h_tag:
        return h_tag.get_text(strip=True) if isinstance(h_tag, Tag) else ""
    h_tag = soup.find('h2')
    if h_tag:
        return h_tag.get_text(strip=True) if isinstance(h_tag, Tag) else ""
    return ""


def get_first_paragraph_from_html(html: str) -> str:
    soup = BeautifulSoup(html, 'html.parser')
    main_tag = soup.find('main')
    if isinstance(main_tag,Tag):
        p_tag = main_tag.find('p')
        if isinstance(p_tag, Tag):
            return p_tag.get_text(strip=True)  
    
    h = soup.find('p')
    return  h.get_text(strip=True) if isinstance(h, Tag) else ""



def get_urls_from_html(html, base_url):
    soup = BeautifulSoup(html,'html.parser')
    
    try:
        res = (list(map(
                lambda x: urljoin(base_url,x),
                list(map(
                        lambda x: x.get('href'),
                        soup.find_all('a')
                        )
                    )
                        )
                )
            )
    except Exception as e:
        return e
    
    return res

def get_images_from_html(html, base_url):
    pass