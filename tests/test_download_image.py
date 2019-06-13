"""
Unittest for script available at ../image_scraper/download_image.py
To run the script:
                python -m unittest tests.test_download_image
"""

import unittest
from unittest.mock import MagicMock, patch, mock_open

from image_scraper.download_image import DownloadImage


class TestDownloadImage(unittest.TestCase):

    def setUp(self):

        filepath1 = '/Users/lokeshtodwal/PycharmProjects/jd/sample_data/test_urls.txt'
        output_dir_path1 = '/Users/lokeshtodwal/PycharmProjects/jd/'
        timestamp = 'timestamp'

        self.download_img1 = DownloadImage(filepath=filepath1, output_dir_path=output_dir_path1, timestamp=timestamp)

        filepath2 = '/this/should/give/file_not_found_error'
        self.download_img2 = DownloadImage(filepath=filepath2, output_dir_path=output_dir_path1, timestamp=timestamp)

        output_dir_path3 = '/this/should/give/not_a_directory_error'
        self.download_img3 = DownloadImage(filepath=filepath1, output_dir_path=output_dir_path3, timestamp=timestamp)

    @patch('image_scraper.download_image.os.path')
    @patch('image_scraper.download_image.os')
    def test_get_urls1(self, mock_os, mock_path):
        mock_path.exists.return_value = True
        mock_path.join.return_value = '/Users/lokeshtodwal/PycharmProjects/jd/timestamp'

        text_file_data = '\n'.join(["demo_url1", "demo_url2", "demo_url3"])
        with patch('builtins.open', mock_open(read_data=text_file_data)) as m:

            m.return_value.__iter__.return_value = text_file_data.splitlines()
            observed_output = self.download_img1.get_urls()

        mock_os.mkdir.assert_called_with('/Users/lokeshtodwal/PycharmProjects/jd/timestamp')

        expected_output = ['demo_url1\n',
                           'demo_url2\n',
                           'demo_url3']

        self.assertEqual(observed_output, expected_output)

    def test_get_urls2(self):
        self.assertRaises(FileNotFoundError, self.download_img2.get_urls)
        self.assertRaises(NotADirectoryError, self.download_img3.get_urls)

    @patch('urllib.request.urlopen')
    @patch('image_scraper.download_image.os.path')
    @patch('image_scraper.download_image.os')
    def test_download_images(self, mock_os, mock_path, mock_urlopen):
        mock_path.exists.return_value = True
        mock_path.join.return_value = '/Users/lokeshtodwal/PycharmProjects/jd/timestamp'

        text_file_data = '\n'.join(["https://www.gstatic.com/webp/kjhm.png"])
        with patch('builtins.open', mock_open(read_data=text_file_data)) as m:
            cm = MagicMock()
            cm.headers['Content-Type'] = 'image/jpeg'
            cm.status = 500
            mock_urlopen.return_value = cm

            m.return_value.__iter__.return_value = text_file_data.splitlines()
            self.download_img1.download_images()
        mock_os.mkdir.assert_called_with('/Users/lokeshtodwal/PycharmProjects/jd/timestamp')

