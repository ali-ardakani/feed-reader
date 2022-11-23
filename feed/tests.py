from django.contrib.auth.models import User
from django.utils import timezone
from mock import Mock
from rest_framework.test import APITestCase

from web_scraping.reddit import RedditScraper

from .models import Category, Feed, Source, CategoryName
from .tasks import updateFeed


class FeedTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(username="testuser",
                                             email="test@test.com",
                                             password="testpassword")
        self.user2 = User.objects.create_user(username="testuser2",
                                              email="test2@test.com",
                                              password="testpassword2")
        self.source = Source.objects.create(
            name="Reddit", url="https://www.reddit.com/r/{category}/.rss")
        categoryName1 = CategoryName.objects.create(name="category1")
        categoryName2 = CategoryName.objects.create(name="category2")
        self.category1 = Category.objects.create(
            name=categoryName1,
            user=self.user,
            )
        self.category1.source.add(self.source)
        self.category2 = Category.objects.create(
            name=categoryName2,
            user=self.user2,
            )
        self.category2.source.add(self.source)
        self.feed1 = Feed.objects.create(
            author="test",
            title="test",
            link="https://www.reddit.com/r/test/comments/9q2q0p/test/",
            published=timezone.now(),
            updated=timezone.now())
        self.feed1.categories.add(self.category1)
        self.feed2 = Feed.objects.create(
            author="test2",
            title="test2",
            link="https://www.reddit.com/r/test/comments/9q2q0p/test2/",
            published=timezone.now(),
            updated=timezone.now())
        self.feed2.categories.add(self.category2)

    def test_create_category(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post("/api/category/create/", {
            "name": "testcategory",
            "source": [self.source.id]
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["name"], "testcategory")
        self.assertEqual(response.data["source"][0], self.source.id)

    def test_create_category_without_source(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post("/api/category/create/", {
            "name": "testcategory",
        })
        self.assertEqual(response.status_code, 400)

    def test_category_list(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/api/category/list/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["name"], "category1")
        self.assertEqual(response.data["results"][0]["source"][0],
                         self.source.id)

    def test_category_info(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f"/api/category/{self.category1.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], "category1")
        self.assertEqual(response.data["source"][0], self.source.id)

    def test_category_delete(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f"/api/category/{self.category1.id}/")
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Category.objects.count(), 1)

    def test_feed_list(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/api/feed/list/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["title"], "test")

    def test_feed_list_category(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/api/feed/list/?category=category1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["title"], "test")

    def test_feed_list_bookmark(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(f"/api/feed/{self.feed1.id}/bookmark/")
        self.assertEqual(response.status_code, 200)
        response = self.client.get("/api/feed/list/?bookmark=true")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["title"], "test")

    def test_feed_retrieve(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f"/api/feed/{self.feed1.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["title"], "test")
        self.assertEqual(response.data["author"], "test")
        self.assertEqual(
            response.data["link"],
            "https://www.reddit.com/r/test/comments/9q2q0p/test/")
        self.assertEqual(
            response.data["published"],
            self.feed1.published.strftime("%Y-%m-%dT%H:%M:%S.%fZ"))
        self.assertEqual(response.data["updated"],
                         self.feed1.updated.strftime("%Y-%m-%dT%H:%M:%S.%fZ"))
        self.assertEqual(response.data["categories"][0], "category1")

    def test_feed_bookmark(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(f"/api/feed/{self.feed1.id}/bookmark/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["bookmarked"], True)
        self.assertEqual(len(self.feed1.bookmarks.all()), 1)
        self.assertEqual(self.feed1.bookmarks.all()[0].user, self.user)

    def test_feed_unbookmark(self):
        self.client.force_authenticate(user=self.user)
        self.client.post(f"/api/feed/{self.feed1.id}/bookmark/")
        response = self.client.post(f"/api/feed/{self.feed1.id}/bookmark/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["bookmarked"], False)
        self.assertEqual(len(self.feed1.bookmarks.all()), 0)

    def test_update_feed_celery_task(self):
        RedditScraper.scrape = Mock(return_value=[
            {
            "author": "test",
            "title": "test",
            "link": "test.com",
            "published": timezone.now(),
            "updated": timezone.now(),
            }
        ])
        task = updateFeed.apply()
        self.assertEqual(task.status, "SUCCESS")