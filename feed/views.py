from rest_framework import status
from rest_framework.generics import (CreateAPIView, ListAPIView,
                                     RetrieveAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Category, Feed
from .pagination import CustomPagination
from .serializers import CategorySerializer, FeedSerializer


class CategoryCreateView(CreateAPIView):
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticated, )


class CategoryListView(ListAPIView):
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticated, )
    pagination_class = CustomPagination

    def get_queryset(self):
        return Category.objects.filter(
            users=self.request.user.id).order_by('name')


class CategoryRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticated, )
    lookup_field = 'pk'

    def get_queryset(self):
        return Category.objects.filter(users=self.request.user.id)


class FeedListView(ListAPIView):
    serializer_class = FeedSerializer
    pagination_class = CustomPagination
    permission_classes = (IsAuthenticated, )
    queryset = Feed.objects.all()

    def get_queryset(self):
        param = {}
        param["categories__name"] = self.request.query_params.get(
            'category', None)
        bookmark = self.request.query_params.get('bookmark', None)
        param[
            "bookmarks__user"] = self.request.user.id if bookmark == "true" else None
        # Delete all none value in param
        param = {k: v for k, v in param.items() if v is not None}
        query = Feed.objects.filter(categories__users=self.request.user.id)
        query = query.filter(**param)

        return query.order_by('-updated')


class FeedRetrieveView(RetrieveAPIView):
    serializer_class = FeedSerializer
    permission_classes = (IsAuthenticated, )
    queryset = Feed.objects.all()

    def get_queryset(self):
        return Feed.objects.filter(categories__users=self.request.user.id)


class BookmarkView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        feed = Feed.objects.filter(pk=pk, categories__users=request.user.id)
        if not feed.exists():
            return Response(status=status.HTTP_404_NOT_FOUND)
        feed = feed.first()
        bookmarked = feed.bookmark(request.user)
        data = FeedSerializer(feed, context={'request': request}).data
        return Response(data=data, status=200)
