import unittest
from crawl import (
    normalize_url, 
    get_heading_from_html, 
    get_first_paragraph_from_html,
    get_urls_from_html,
    get_images_from_html,
    extract_page_data
    )

class TestCrawl(unittest.TestCase):
    def test_normalize_https_url_with_trailing_slash(self):
        input_url = "https://www.boot.dev/blog/path/"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)
    def test_normalize_https_url_without_trailing_slash(self):
        input_url = "https://www.boot.dev/blog/path"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)
    def test_normalize_http_url_with_trailing_slash(self):
        input_url = "http://www.boot.dev/blog/path/"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)
    def test_normalize_http_url_without_trailing_slash(self):
        input_url = "http://www.boot.dev/blog/path"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)     
    def test_already_normalized_url(self):
        input_url = "www.boot.dev"       
        actual = normalize_url(input_url)
        expected = "www.boot.dev"
        self.assertEqual(actual, expected)
    def test_empty_url(self):
        input_url = ""       
        actual = normalize_url(input_url)
        expected = ""
        self.assertEqual(actual, expected)
    def test_no_protocol_url(self):
        input_url = "boot.dev"       
        actual = normalize_url(input_url)
        expected = "boot.dev"
        self.assertEqual(actual, expected)
    def test_path_no_protocol(self):
        input_url = "boot.dev/path".title()
        actual = normalize_url(input_url)
        expected = "boot.dev/path"
        self.assertEqual(actual, expected)
    def test_path_no_protocol_trailing_slash(self):
        input_url = "boot.dev/path/".capitalize()
        actual = normalize_url(input_url)
        expected = "boot.dev/path"
        self.assertEqual(actual, expected)
    def test_full_url(self):
        input_url = "http://testuser:testpass@testdomain.com:8080/testpath?testsearch=testvalue#testhash"
        actual = normalize_url(input_url)
        expected = "testuser:testpass@testdomain.com:8080/testpath"
        self.assertEqual(actual, expected)

    # Root path: https://www.boot.dev/
    def test_root_path(self):
        input_url = "https://www.boot.dev/"
        actual = normalize_url(input_url)
        expected = "www.boot.dev"
        self.assertEqual(actual, expected)
    # Query only: https://www.boot.dev?x=1
    def test_query_only(self):
        input_url = "https://www.boot.dev?x=1"
        actual = normalize_url(input_url)
        expected = "www.boot.dev"
        self.assertEqual(actual, expected)
    # Fragment only: https://www.boot.dev#top
    def test_fragment_only(self):
        input_url = "https://www.boot.dev#top"
        actual = normalize_url(input_url)
        expected = "www.boot.dev"
        self.assertEqual(actual, expected)
    # Credentials and port: http://user:pass@boot.dev:8080/path
    def test_credentials_and_port(self):
        input_url = "http://user:pass@boot.dev:8080/path"
        actual = normalize_url(input_url)
        expected = "user:pass@boot.dev:8080/path"
        self.assertEqual(actual, expected)
   


    

    def test_get_h1(self):
        input_body = "<html><body><h1>Test Title</h1></body></html>"
        actual = get_heading_from_html(input_body)
        expected = "Test Title"
        self.assertEqual(actual, expected)


    def test_get_h2_whitespaces(self):
        input_body = "<html><body><h2>Test Title in h2   </h2></body></html>"
        actual = get_heading_from_html(input_body)
        expected = "Test Title in h2"
        self.assertEqual(actual, expected)

    def test_get_h3(self):
        input_body = "<html><body><h3>Test Title in h3</h3></body></html>"
        actual = get_heading_from_html(input_body)
        expected = ""
        self.assertEqual(actual, expected)



    def test_get_first_paragraph_from_html_main_priority(self):
        input_body = """<html><body>
            <p>Outside paragraph.</p>
            <main>
                <p>Main paragraph.</p>
            </main>
        </body></html>"""
        actual = get_first_paragraph_from_html(input_body)
        expected = "Main paragraph."
        self.assertEqual(actual, expected)
    def test_get_paragraph_out_main_with_no_paragraph_inside(self):
        input_body = """<html><body>
            <p>Outside paragraph.</p>
            <main>
               <div>Content</div>
            </main>
        </body></html>"""
        actual = get_first_paragraph_from_html(input_body)
        expected = "Outside paragraph."
        self.assertEqual(actual, expected)
    def test_no_paragraph(self):
        input_body = "<html><body><h2>Test Title in h2</h2></body></html>"
        actual = get_first_paragraph_from_html(input_body)
        expected = ""
        self.assertEqual(actual, expected)
    def test_get_first_paragraph_out_html_main_priority(self):
        input_body = """<html><body>
            <p>Outside paragraph.</p>            
        </body></html>"""
        actual = get_first_paragraph_from_html(input_body)
        expected = "Outside paragraph."
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_absolute(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a href="https://crawler-test.com"><span>Boot.dev</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com"]
        self.assertEqual(actual, expected)
    def test_get_urls_absolute_and_relative(self):
        input_url = "https://absolute.com"
        input_body = '''<html><body> 
                        <a href="https://absolute.com"><span>Boot.dev</span></a> 
                        <a href="/relative"><span>Boot.dev/relative</span></a>
                    </body></html>'''
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://absolute.com","https://absolute.com/relative"]
        self.assertEqual(actual, expected)

    def test_get_urls_no_href(self):
        input_url = "http://vacuum.org"
        input_body = '<html><body><img src="/logo.png" alt="Logo"></body></html>'
        actual = get_urls_from_html(input_body,input_url)
        expected = []
        self.assertEqual(actual,expected)
    def test_get_urls_from_html_both(self) -> None:
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a href="/path/one"><span>Boot.dev</span></a><a href="https://other.com/path/one"><span>Boot.dev</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/path/one", "https://other.com/path/one"]
        self.assertEqual(actual, expected)

    # ***IMAGES***
    def test_get_images_from_html_relative(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img src="/logo.png" alt="Logo"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/logo.png"]
        self.assertEqual(actual, expected)  

    def test_get_no_images(self):
        input_url = "https://crawler-test.com"
        input_body = '''<html><body> 
                        <a href="https://absolute.com"><span>Boot.dev</span></a> 
                        <a href="/relative"><span>Boot.dev/relative</span></a>
                    </body></html>'''
        actual = get_images_from_html(input_body, input_url)
        expected = []
        self.assertEqual(actual, expected)  
    
    def test_get_images_nested(self):
        input_url = "https://example.com"
        input_body = '''<html>
                                <body>
                                    <div>
                                    <p>
                                        Look at logo:
                                        <img src="/logo.png" alt="Logo" />
                                    </p>
                                    </div>
                                    <a href="/home">
                                    <img src="https://example.com/icon.png" alt="Icon" />
                                    </a>
                                </body>
                                </html>'''
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://example.com/logo.png", "https://example.com/icon.png"]
        self.assertEqual(actual, expected)  


    # TEST EXTRACT PAGES
    def test_extract_page_data_basic(self):
        input_url = "https://crawler-test.com"
        input_body = """<html><body>
            <h1>Test Title</h1>
            <p>This is the first paragraph.</p>
            <a href="/link1">Link 1</a>
            <img src="/image1.jpg" alt="Image 1">
        </body></html>"""
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "Test Title",
            "first_paragraph": "This is the first paragraph.",
            "outgoing_links": ["https://crawler-test.com/link1"],
            "image_urls": ["https://crawler-test.com/image1.jpg"],
        }
        self.assertEqual(actual, expected)
    


    def test_extract_page_data_h2_and_multi_assets(self):
        input_url = "https://crawler-test.com"
        input_body = """<html><body>
            <h2>Test Title</h2>
            <p>This is the first paragraph </p>
            <img src="/fig1.png" alt="fig1" />
            <a href="/link1">Link 1</a>
            <a href="/link2">Link 2</a>
            <img src="/image2.jpg" alt="Image 2">
        </body></html>"""
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "Test Title",
            "first_paragraph": "This is the first paragraph",
            "outgoing_links": ["https://crawler-test.com/link1","https://crawler-test.com/link2"],
            "image_urls": ["https://crawler-test.com/fig1.png","https://crawler-test.com/image2.jpg"],
        }
        self.assertEqual(actual, expected)
    def test_extract_page_data_main_section(self) -> None:
        input_url = "https://crawler-test.com"
        input_body = """<html><body>
            <nav><p>Navigation paragraph</p></nav>
            <main>
                <h1>Main Title</h1>
                <p>Main paragraph content.</p>
            </main>
        </body></html>"""
        actual = extract_page_data(input_body, input_url)
        self.assertEqual(actual["heading"], "Main Title")
        self.assertEqual(actual["first_paragraph"], "Main paragraph content.")

    def test_extract_page_data_missing_elements(self) -> None:
        input_url = "https://crawler-test.com"
        input_body = "<html><body><div>No h1, p, links, or images</div></body></html>"
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "",
            "first_paragraph": "",
            "outgoing_links": [],
            "image_urls": [],
        }
        self.assertEqual(actual, expected)




if __name__ == "__main__":
    unittest.main()