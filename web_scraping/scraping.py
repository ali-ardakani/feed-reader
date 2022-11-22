from abc import ABC, abstractmethod
from typing import Dict, List

import requests


class Request:

    @staticmethod
    def get(url: str) -> str:
        """
        Get the content of the url
        """
        # TODO: Validate url
        try:
            response = requests.get(url)
            return response.text
        except requests.exceptions.MissingSchema:
            # TODO: Handle this exception
            return ""
        except requests.exceptions.ConnectionError:
            # TODO: Handle this exception
            return ""


class RSSScraper(ABC):
    """
    Abstract base class for all scrapers
    """

    def __init__(self, url: str):
        self.url = url
        self.content = Request.get(url)

    @abstractmethod
    def scrape(self, limit: int) -> List[Dict]:
        """
        Abstract method for scraping
        
        :param limit: Number of posts to scrape(default: all)
        :return: List of posts (must include author, title, link, published, updated)
        """
        pass
