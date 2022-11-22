from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

from feed.models import Source
from web_scraping import ScraperFactory


class Command(BaseCommand):
    help = 'Initialize the database'

    def handle(self, *args, **options):
        for source in ScraperFactory.SOURCES:
            try:
                Source.objects.get_or_create(name=source["name"],
                                             url=source["url"])
            except IntegrityError:
                pass
        self.stdout.write(
            self.style.SUCCESS('Successfully initialized the database'))
