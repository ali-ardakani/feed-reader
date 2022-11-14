from .models import Feed
from celery import shared_task

#Implement a back-off mechanism in case the system fails to update the feed.
@shared_task(bind=True, max_retries=3)
def update_feed(self, pk: int, user_id: int, title: str):
    try:
        feed = Feed.objects.get(pk=pk)
        if feed.user.id != user_id:
            raise Exception("User mismatch")
        feed.title = title
        feed.save()
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)
    
        