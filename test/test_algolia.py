import unittest

from src.algolia import search_designers, search_fragrance

class TestAlgolia(unittest.TestCase):
    def test_designer(self):
        result = search_designers("Jean Paul Gaultier")
        # Failure of the below test probably means that search API has changed
        # to fix: open fragrantica.com, type something in the search field, in dev tools open Network->Payload and copy x-algolia-api-key value. Put it in src/algolia.py
        self.assertGreater(len(result), 0)
        self.assertEqual(result[0]['brand'], "Jean Paul Gaultier")

    def test_fragrance(self):
        designer = search_designers("Jean Paul Gaultier")
        result = search_fragrance(designer[0]['brand'], "Le Male Le Parfum")
        self.assertGreater(len(result), 0)
        self.assertEqual(result[0]['name'], "Le Male Le Parfum")
        # print(frags)

if __name__ == "__main__":
    unittest.main()