"""
Below class pre-process the url list assigned to it.
"""

from posixpath import basename
from urllib.parse import urlparse


class PreProcessURLs:

    def __init__(self, url_list):
        """
        :param url_list: List of the URL
        """

        self.url_list = url_list

    def remove_eol_characters(self):
        """
        Remove the EOL characters
        :return: list where eol characters are removed from each element
        """

        return [url.strip() for url in self.url_list]

    @staticmethod
    def remove_empty_elements(url_list):
        """
        Removes empty element from the list
        :param url_list: List of the URL
        :return: list where empty elements are removed from the list
        """

        return [url for url in url_list if url]

    @staticmethod
    def remove_duplicate_elements(url_list):
        """
        Removes the duplicate elements from the list
        :param url_list:  List of the URL
        :return: list where duplicate elements are removed from the list
        """

        return list(set(url_list)), len(set(url_list))

    def pre_process_urls(self):
        """
        Cleans the URL
        :return: clean_url_list: Removes EOL chars, empty elements, duplicate elements.
                 duplicate_url_count: Count the duplicate elements.
        """

        # Removes EOL characters
        url_list = self.remove_eol_characters()

        # Removes empty element from the list
        clean_url_list = self.remove_empty_elements(url_list)

        # Total number of URLs present in the file
        total_url_count = len(clean_url_list)

        # Removes the duplicate elements from the list
        clean_url_list, uniq_url_count = self.remove_duplicate_elements(clean_url_list)

        # Get the duplicate urls count
        duplicate_url_count = total_url_count - uniq_url_count

        return clean_url_list, duplicate_url_count


"""
Below class validates the URL
"""


class URLValidator:
    def __init__(self):
        """
        Counter which will be used when the images does not have base image.
        Ex: https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTQVAKOMUULIBcWwo1e1Ci6sJnn1PfoKVEfXjSYUnSuGV61WWk9
        When downloading these kind of file we will observe that the files are saving in the name of `images(*).png`
        """

        self.counter = 0

    @staticmethod
    def is_schema_contains_data(parsed_url):
        """
        Check if scheme is present in the data
        :param parsed_url: Parsed URL
        :return: Bool: If scheme is present: True, Else: False
        """

        return bool(parsed_url.scheme)

    @staticmethod
    def is_netloc_contains_data(parsed_url):
        """
        Check if netloc is present in the data
        :param parsed_url: Parsed URL
        :return: Bool: If netloc is present: True, Else: False
        """

        return bool(parsed_url.netloc)

    @staticmethod
    def is_image_path_valid(parsed_url):
        """
        Checks if the parsed URL path ends with ('jpg', 'png', 'gif', 'bmp', 'jpeg', 'webp') or startswith 'images'
        :param parsed_url: Parsed URL
        :return: Bool: True if it any condition is True, Else False
        """

        return (parsed_url.path.endswith(('jpg', 'png', 'gif', 'bmp', 'jpeg', 'webp'))
                or parsed_url.path.startswith('/images'))

    def is_image_url_valid(self, url):
        """
        Checks if the url is valid
        :param url: Parsed URL
        :return: True if all of the conditions are True, Else False
        """

        parsed_url = urlparse(url)

        return bool(self.is_schema_contains_data(parsed_url)
                    and self.is_netloc_contains_data(parsed_url)
                    and self.is_image_path_valid(parsed_url))

    def get_basename(self, url):
        """
        Get the base name of the image from URL
        :param url: URL of the (str)
        :return: image_name (str)
        """

        parsed_url = urlparse(url)

        if parsed_url.path.endswith(('jpg', 'png', 'gif', 'bmp', 'jpeg', 'webp')):
            return basename(parsed_url.path)

        elif parsed_url.path.startswith('/images'):
            self.counter = self.counter + 1
            return 'images.png' if self.counter == 1 else 'images{}.png'.format(self.counter)
