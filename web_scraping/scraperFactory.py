from .scraping import RSSScraper
from .reddit import RedditScraper


class ScraperFactory:

    SOURCES = [
        {
            "name": "Reddit",
            "url": "https://www.reddit.com/r/{category}/.rss",
            "scraper": RedditScraper,
        },
    ]

    @staticmethod
    def createScraper(url: str, category: str) -> RSSScraper:
        """
        Create a scraper based on the url
        
        :param url: Url of the website
        :param category: Category of the website
        :return: Scraper
        """
        for source in ScraperFactory.SOURCES:
            if url == source["url"]:
                return source["scraper"](url.format(category=category))