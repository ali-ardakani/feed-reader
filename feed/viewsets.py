from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .serializers import FeedSerializer
from rest_framework import viewsets
from .models import Feed
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .tasks import update_feed

class FeedViewSet(viewsets.ViewSet):
    
    permission_classes = (IsAuthenticated,)
    
    def list(self, request):
        queryset = Feed.objects.all()
        serializer = FeedSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Feed.objects.all()
        feed = get_object_or_404(queryset, pk=pk)
        serializer = FeedSerializer(feed)
        return Response(serializer.data)

    def create(self, request):
        serializer = FeedSerializer(data={"user": request.user.id, "title": request.data["title"]})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        res = update_feed.delay(pk, request.user.id, request.data["title"])
        return Response(status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, pk=None):
        feed = Feed.objects.filter(pk=pk)
        if not feed.exists():
            return Response({ "error": "Feed not found" }, status=status.HTTP_404_NOT_FOUND)
        feed = feed.first()
        if feed.user.id != request.user.id:
            return Response({ "error": "User mismatch" }, status=status.HTTP_403_FORBIDDEN)
        data = FeedSerializer(feed).data
        feed.delete()
        return Response(data=data, status=status.HTTP_200_OK)