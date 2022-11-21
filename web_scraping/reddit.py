from typing import Dict, List

from bs4 import BeautifulSoup

from .scraping import RSSScraper


class RedditScraper(RSSScraper):
    """
    Scraper for reddit.com
    """

    def scrape(self, limit: int = 0) -> List[Dict]:
        """
        Scrape all posts from a given category on reddit.com
        
        :param limit: Number of posts to scrape(default: all)
        :return: List of posts
        """
        posts = []

        soup = BeautifulSoup(self.content, "xml")

        items = soup.find_all("entry")
        # Limit the number of posts
        if limit > 0:
            items = items[:limit]

        for item in items:
            author = item.find("author")

            posts.append({
                "author_name":
                author.find("name").text.replace("/u/", ""),
                "author_uri":
                author.find("uri").text,
                "title":
                item.find("title").text,
                "link":
                item.find("link")["href"],
            })

        return posts