from .scraping import RSSScraper
from .reddit import RedditScraper


class ScraperFactory:

    @staticmethod
    def create_scraper(url: str, category: str) -> RSSScraper:
        """
        Create a scraper based on the url
        """
        if "reddit.com" in url:
            url = f"{url}/r/{category}/.rss"
            return RedditScraper(url)
        else:
            raise NotImplementedError("Scraper not implemented")