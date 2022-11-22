from celery import shared_task
from celery.utils.log import get_task_logger

from feed.models import Category, Feed
from web_scraping import ScraperFactory

logger = get_task_logger(__name__)


@shared_task
def updateFeed():
    """
    Update the feed
    """
    for category in Category.objects.all():
        for source in category.source.all():
            scraper = ScraperFactory.createScraper(source.url, category.name)
            for feed in scraper.scrape():
                feed, created = Feed.objects.get_or_create(
                    defaults={
                        "link": feed["link"],
                    },
                    author=feed["author"],
                    title=feed["title"],
                    published=feed["published"],
                    updated=feed["updated"],
                )
                feed.categories.add(category)

    return "Feed updated"