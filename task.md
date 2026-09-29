write more edge cases tests #TODO

DONE

0� [ ] Create a file called `crawl.py` and stub a function called `normalize_url`.
0� [ ] Create a file called `test_crawl.py` in the root of your project.
    The `uv run -m unittest` command will discover and run tests for files that start with `test`.
0� [ ] Write a few tests! Remember, this function should take a single URL (string) and return the normalized version of the URL as a string. This will help us later to detect whether two different URLs point to the same  *web page* , which is all our users care about. Here's a single [example unit test](https://docs.python.org/3/library/unittest.html#basic-example) to get you started:

    ```py
    import unittest
    from crawl import normalize_url

    class TestCrawl(unittest.TestCase):
        def test_normalize_url(self):
            input_url = "https://www.boot.dev/blog/path"
            actual = normalize_url(input_url)
            expected = "www.boot.dev/blog/path"
            self.assertEqual(actual, expected)



    if __name__ == "__main__":
        unittest.main()
    ```

        **
          **

    Try to test all the [edge-cases](https://en.wikipedia.org/wiki/Edge_case) you can think of.
0� [ ] Run your tests. `uv run -m unittest` will run all the tests in the current directory.
    You should see some *failing tests* now, which is expected because you haven't filled in the `normalize_url` function yet.
0� [ ] Write the `normalize_url` function. I recommend using the [`urlsplit`](https://docs.python.org/3/library/urllib.parse.html#urllib.parse.urlsplit) function from the `urllib.parse` package. It parses a raw URL string into a URL object with some fields like `netloc` and `path`, which will be useful to you.

**Run and submit** the CLI tests from the  **root of the module** .
