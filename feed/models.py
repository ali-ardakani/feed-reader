from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import (GenericForeignKey,
                                                GenericRelation)
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Source(models.Model):
    name = models.CharField(max_length=255, unique=True)
    url = models.URLField(unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    users = models.ManyToManyField(User, related_name="categories", blank=True)
    source = models.ManyToManyField(Source, related_name="categories")
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()


class AbilityToBookmark(models.Model):
    bookmarks = GenericRelation(Bookmark)

    def bookmark(self, user):
        if self.bookmarks.filter(user=user).exists():
            self.bookmarks.filter(user=user).delete()
            return False
        else:
            Bookmark.objects.create(user=user, content_object=self)
            return True

    class Meta:
        abstract = True


class Feed(AbilityToBookmark):
    author = models.CharField(max_length=255, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    link = models.URLField(unique=True)
    published = models.DateTimeField(null=True, blank=True)
    updated = models.DateTimeField(null=True, blank=True)
    categories = models.ManyToManyField(Category, related_name="feeds")

    def __str__(self):
        return self.title