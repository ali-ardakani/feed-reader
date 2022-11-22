from django.urls import path, re_path

from .views import (BookmarkView, CategoryCreateView, CategoryListView,
                    CategoryRetrieveUpdateDestroyView, FeedListView,
                    FeedRetrieveView)

urlpatterns = [
    path('category/create/', CategoryCreateView.as_view()),
    path('category/list/', CategoryListView.as_view()),
    path('category/<int:pk>/', CategoryRetrieveUpdateDestroyView.as_view()),
    re_path(r'^feed/list/$', FeedListView.as_view()),
    path('feed/<int:pk>/', FeedRetrieveView.as_view()),
    path('feed/<int:pk>/bookmark/', BookmarkView.as_view()),
]