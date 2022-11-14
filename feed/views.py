from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Feed
from .serializers import FeedSerializer


class BookmarkView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        feed = Feed.objects.get(pk=pk)
        bookmarked = feed.bookmark(request.user)
        data = FeedSerializer(feed).data
        return Response(data=data, status=200)