"""
Downloads the image from URLs
1. Read text file.
2. Pre-process the URLs to remove EOL characters and empty elements.
3. Validate the URL.
4. Download the image is certain directory.

to run: `python -m image_scraper.download_image --filepath sample_data/urls.txt
                                                --output_dir_path /Users/lokeshtodwal/Downloads`
        or `python -m image_scraper.download_image --filepath sample_data/urls.txt` (takes current default directory
                                                                                     as output directory path)
"""

import logging
import os
import shutil
import urllib
import urllib.request
from datetime import datetime

import click

from .utils import PreProcessURLs, URLValidator

click.disable_unicode_literals_warning = True


class DownloadImage:
    def __init__(self, filepath, output_dir_path, timestamp):
        """
        :param filepath: Source file path where the text file is placed
        :param output_dir_path: Dir where image files will be downloaded.
        :param timestamp: timestamp at which script has run
        """

        self.filepath = filepath
        self.output_dir_path = output_dir_path
        self.timestamp = timestamp

    def get_urls(self):
        """
        Retrieves list of URLs from text file.
        :return: list of URLs
        """

        if not os.path.exists(self.filepath):
            raise FileNotFoundError(self.filepath)

        if not os.path.exists(self.output_dir_path):
            raise NotADirectoryError(self.output_dir_path)
        else:
            # Create a new dir inside output dir path where all the images will be saved
            os.mkdir(os.path.join(self.output_dir_path, self.timestamp))
            logging.basicConfig(filename=os.path.join(os.path.join(self.output_dir_path,
                                                                   self.timestamp), 'logger.log'),
                                filemode='a',
                                format='%(asctime)s %(name)s: %(levelname)s::: %(message)s',
                                level=logging.INFO)
            self.logger = logging.getLogger(__name__)

        with open(self.filepath, 'r') as fp:
            url_list = fp.readlines()

        return url_list

    def download_images(self):
        """
        Downloads the images
        :return: None
        """

        # Retrieve url list
        url_list = self.get_urls()

        # Pre-processing the urls, removing EOL characters, empty elements and duplicate elements.
        pre_process_url = PreProcessURLs(url_list=url_list)
        clean_url_list, duplicate_urls_count = pre_process_url.pre_process_urls()
        self.logger.info("Removed {} duplicate elements.".format(duplicate_urls_count))

        # Creating url validator object
        validator = URLValidator()

        total_success = 0
        total_failure = 0

        for url in clean_url_list:

            # Checking if url of image is valid or not
            if validator.is_image_url_valid(url=url):
                # Getting basename or the filename of the image from URL
                image_name = validator.get_basename(url=url)

                try:
                    image_path = os.path.join(self.output_dir_path, self.timestamp, image_name)

                    # Getting the response from the URL
                    response = urllib.request.urlopen(url)

                    # Checking if the content-type is image or not and status code is 200 or not
                    if response.headers['Content-Type'].startswith('image') and response.status == 200:

                        # Opening the image file and writing the response in it.
                        with open(image_path, "wb") as file:
                            shutil.copyfileobj(response, file)

                        self.logger.info('URL scraping successful for: {}'.format(url))

                        total_success += 1
                    else:
                        # If the response condition does not satisfy
                        self.logger.info('URL scraping failed for: {}'.format(url))
                        total_failure += 1

                except urllib.error.URLError:
                    # If the server is offline or web page no longer exist
                    self.logger.info('URL scraping failed for: {}'.format(url))
                    total_failure += 1

            else:
                self.logger.info('Invalid image URL: {}'.format(url))
                total_failure += 1

        self.logger.info("## BINGO ## URL scraping completed with {} successes and {} failures.".format(total_success,
                                                                                                        total_failure))


@click.command()
@click.option("--filepath", prompt="Enter file path", help="Path of the file")
@click.option("--output_dir_path", default='.', help="Path at which all the images will be saved")
def get_download(filepath, output_dir_path):

    # Calling `DownloadImage` class
    timestamp = datetime.now().strftime('%Y-%m-%d__%H:%M:%S')
    down = DownloadImage(filepath=filepath, output_dir_path=output_dir_path, timestamp=timestamp)
    down.download_images()


if __name__ == '__main__':
    get_download()
