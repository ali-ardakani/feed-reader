from rest_framework import serializers
from .models import Feed
from django.contrib.auth.models import User

class FeedSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Feed
        fields = ('user', 'title')
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["user"] = instance.user.username
        representation["bookmarked"] = instance.bookmarks.filter(user=instance.user).exists()
        return representation