from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.auth.models import User


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
            Bookmark.objects.create(
                user=user,
                content_object=self
            )
            return True
        
    class Meta:
        abstract = True


class Feed(AbilityToBookmark):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title