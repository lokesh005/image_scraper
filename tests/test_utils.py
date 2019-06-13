"""
Unittest for script available at ../image_scraper/utils.py
To run the script:
                python -m unittest tests.test_utils
"""

import unittest
from urllib.parse import urlparse

from image_scraper.utils import PreProcessURLs, URLValidator


class TestUtils(unittest.TestCase):

    def setUp(self):
        url_list = ['https://www.gstatic.com/webp/gallery3/1_webp_ll.sm.png\n   ',
                    'https://www.gstatic.com/webp/gallery/4.sm.webp\n ',
                    'https://www.gstatic.com/webp/gallery3/3_webp_ll.sm.png\n',
                    '   https://www.gstatic.com/webp/gallery3/4_webp_ll.sm.png\n',
                    'https://www.gstatic.com/webp/gallery3/5.sm.png\n',
                    '  https://res.cloudinary.com/demo/image/upload/q_60/sample.jpg\n  ',
                    '   ',
                    'https://res.cloudinary.com/demo/image/upload/q_60/sample.jpg\n']
        self.preprocess_urls = PreProcessURLs(url_list=url_list)

    def test_remove_eol_characters(self):
        observed_result = self.preprocess_urls.remove_eol_characters()

        expected_result = ['https://www.gstatic.com/webp/gallery3/1_webp_ll.sm.png',
                           'https://www.gstatic.com/webp/gallery/4.sm.webp',
                           'https://www.gstatic.com/webp/gallery3/3_webp_ll.sm.png',
                           'https://www.gstatic.com/webp/gallery3/4_webp_ll.sm.png',
                           'https://www.gstatic.com/webp/gallery3/5.sm.png',
                           'https://res.cloudinary.com/demo/image/upload/q_60/sample.jpg',
                           '',
                           'https://res.cloudinary.com/demo/image/upload/q_60/sample.jpg']

        self.assertListEqual(observed_result, expected_result)

    def test_remove_empty_elements(self):
        result_list = self.preprocess_urls.remove_eol_characters()
        observed_result = self.preprocess_urls.remove_empty_elements(result_list)

        expected_result = ['https://www.gstatic.com/webp/gallery3/1_webp_ll.sm.png',
                           'https://www.gstatic.com/webp/gallery/4.sm.webp',
                           'https://www.gstatic.com/webp/gallery3/3_webp_ll.sm.png',
                           'https://www.gstatic.com/webp/gallery3/4_webp_ll.sm.png',
                           'https://www.gstatic.com/webp/gallery3/5.sm.png',
                           'https://res.cloudinary.com/demo/image/upload/q_60/sample.jpg',
                           'https://res.cloudinary.com/demo/image/upload/q_60/sample.jpg']

        self.assertListEqual(observed_result, expected_result)

    def test_remove_duplicate_elements(self):
        removed_eol_list = self.preprocess_urls.remove_eol_characters()
        removed_empty_list = self.preprocess_urls.remove_empty_elements(removed_eol_list)

        observed_result, observed_uniq_url_count = self.preprocess_urls.remove_duplicate_elements(removed_empty_list)

        expected_result = ['https://www.gstatic.com/webp/gallery3/1_webp_ll.sm.png',
                           'https://www.gstatic.com/webp/gallery/4.sm.webp',
                           'https://www.gstatic.com/webp/gallery3/3_webp_ll.sm.png',
                           'https://www.gstatic.com/webp/gallery3/4_webp_ll.sm.png',
                           'https://www.gstatic.com/webp/gallery3/5.sm.png',
                           'https://res.cloudinary.com/demo/image/upload/q_60/sample.jpg']

        self.assertEqual(set(observed_result), set(expected_result))
        self.assertEqual(observed_uniq_url_count, 6)

    def test_pre_process_urls(self):
        observed_result, observed_duplicate_url_count = self.preprocess_urls.pre_process_urls()

        expected_result = ['https://www.gstatic.com/webp/gallery3/1_webp_ll.sm.png',
                           'https://www.gstatic.com/webp/gallery/4.sm.webp',
                           'https://www.gstatic.com/webp/gallery3/3_webp_ll.sm.png',
                           'https://www.gstatic.com/webp/gallery3/4_webp_ll.sm.png',
                           'https://www.gstatic.com/webp/gallery3/5.sm.png',
                           'https://res.cloudinary.com/demo/image/upload/q_60/sample.jpg']

        self.assertEqual(set(observed_result), set(expected_result))
        self.assertEqual(observed_duplicate_url_count, 1)


class TestUtilsURLValidator(unittest.TestCase):

    def setUp(self):
        self.url1 = 'https://www.gstatic.com/webp/gallery3/1_webp_ll.sm.png'
        self.url2 = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTQVAKOMUULIBcWwo1' \
                    'e1Ci6sJnn1PfoKVEfXjSYUnSuGV61WWk9'
        self.url_validator = URLValidator()
        self.parsed_url = urlparse(self.url1)

    def test_is_schema_contains_data(self):
        observed_output = self.url_validator.is_schema_contains_data(self.parsed_url)

        self.assertTrue(observed_output)

    def test_is_netloc_contains_data(self):
        observed_output = self.url_validator.is_netloc_contains_data(self.parsed_url)

        self.assertTrue(observed_output)

    def test_is_image_path_valid(self):
        observed_output = self.url_validator.is_image_path_valid(self.parsed_url)

        self.assertTrue(observed_output)

    def test_is_image_url_valid(self):
        observed_output = self.url_validator.is_image_url_valid(self.url1)

        self.assertTrue(observed_output)

    def test_get_basename(self):
        observed_output1 = self.url_validator.get_basename(self.url1)
        expected_output1 = '1_webp_ll.sm.png'

        self.assertEqual(observed_output1, expected_output1)

        observed_output2 = self.url_validator.get_basename(self.url2)
        expected_output2 = 'images.png'

        self.assertEqual(observed_output2, expected_output2)


if __name__ == '__main__':
    unittest.main()
