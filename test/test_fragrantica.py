import unittest
import os
from cleanup import TempFiles
from src.fragrantica import html_to_soup, get_fragrantica_html


class TestFragrantica(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp_files = TempFiles()

        cls.html_file = os.path.abspath("./temp.html")
        cls.temp_files.add_file(cls.html_file)

    @classmethod
    def tearDownClass(cls):
        cls.temp_files.cleanup()

    def test_beautifulsoup(self):
        link = "https://www.fragrantica.com/perfume/Xerjoff/Uden-6306.html"
        html = get_fragrantica_html(link)
        with open(os.path.abspath("./temp.html"), "w") as file:
            file.write(html)
        self.assertTrue(os.path.exists(os.path.abspath("./temp.html")))
        self.assertLess(os.path.getsize(os.path.abspath("./temp.html")), 100000)

        soup = html_to_soup(html)
        images = soup.find_all("meta", property="og:image")
        self.assertGreater(len(images), 0)
        
        