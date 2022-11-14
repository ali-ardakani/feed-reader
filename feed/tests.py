from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Feed
from django.test.utils import override_settings
from celery.contrib.testing import tasks
from .tasks import update_feed
from celery.contrib.testing.worker import start_worker


class FeedTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(username="testuser",
                                             email="test@test.com",
                                                password="testpassword")
        self.user2 = User.objects.create_user(username="testuser2",
                                                email="test2@test.com",
                                                password="testpassword2")
        self.feed = Feed.objects.create(user=self.user, title="testfeed")
    
    def test_feed_list(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/api/feed/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "testfeed")
        self.assertEqual(response.data[0]["user"], "testuser")
         
    def test_feed_create(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post("/api/feed/create/", {"title": "testfeed2"})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["title"], "testfeed2")
        self.assertEqual(response.data["user"], "testuser")
        
    def test_feed_retrieve(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f"/api/feed/{self.feed.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["title"], "testfeed")
        self.assertEqual(response.data["user"], "testuser")
        
    @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
    def test_feed_update(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.put(f"/api/feed/{self.feed.id}/", {"title": "testfeed2"})
        self.assertEqual(response.status_code, 202)
        self.feed.refresh_from_db()
        self.assertEqual(self.feed.title, "testfeed2")
        
    
    @override_settings(CELERY_TASK_ALWAYS_EAGER=True, CELERY_TASK_EAGER_PROPAGATES_EXCEPTIONS=True)
    def test_feed_update_fail(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.put(f"/api/feed/{self.feed.id}/", {"title": "testfeed2"})
        self.assertEqual(response.status_code, 202)
        self.feed.refresh_from_db()
        self.assertEqual(self.feed.title, "testfeed2")
        self.feed.user = User.objects.create_user(username="testuser3",
                                                email="test3@test.com",
                                                password="testpassword3")
        self.feed.save()
        response = self.client.put(f"/api/feed/{self.feed.id}/", {"title": "testfeed3"})
        self.feed.refresh_from_db()
        self.assertEqual(self.feed.title, "testfeed2")
        
    def test_feed_bookmark(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(f"/api/feed/{self.feed.id}/bookmark/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["bookmarked"], True)
        self.assertEqual(len(self.feed.bookmarks.all()), 1)
        self.assertEqual(self.feed.bookmarks.all()[0].user, self.user)
    
    def test_feed_unbookmark(self):
        self.client.force_authenticate(user=self.user)
        self.client.post(f"/api/feed/{self.feed.id}/bookmark/")
        response = self.client.post(f"/api/feed/{self.feed.id}/bookmark/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["bookmarked"], False)
        self.assertEqual(len(self.feed.bookmarks.all()), 0)
    
    def test_feed_delete_fail(self):
        self.client.force_authenticate(user=self.user2)
        response = self.client.delete(f"/api/feed/{self.feed.id}/")
        self.assertEqual(response.status_code, 403)
        self.assertEqual(len(Feed.objects.all()), 1)

    def test_feed_delete(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f"/api/feed/{self.feed.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(Feed.objects.all()), 0)
        