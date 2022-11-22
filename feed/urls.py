from django.urls import path
from .viewsets import FeedViewSet
from .views import BookmarkView

urlpatterns = [
    path('', FeedViewSet.as_view({'get': 'list'})),
    path('<int:pk>/', FeedViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'})),
    path('create/', FeedViewSet.as_view({'post': 'create'})),
    path('<int:pk>/bookmark/', BookmarkView.as_view()),
]