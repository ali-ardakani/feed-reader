from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Category, Feed
from .serializers import CategorySerializer, FeedSerializer

# from .tasks import update_feed


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticated, )
    queryset = Category.objects.all()

    def list(self, request):
        queryset = Category.objects.filter(users=request.user.id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class FeedViewSet(viewsets.ViewSet):
    serializer_class = FeedSerializer
    permission_classes = (IsAuthenticated, )
    queryset = Feed.objects.all()

    # def list(self, request):
    #     queryset = Feed.objects.all()
    #     serializer = FeedSerializer(queryset, many=True)
    #     return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Feed.objects.all()
        feed = get_object_or_404(queryset, pk=pk)
        serializer = FeedSerializer(feed)
        return Response(serializer.data)