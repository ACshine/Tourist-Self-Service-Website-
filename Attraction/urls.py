from django.urls import path
from .views import (
    AttractionListCreateAPIView,
    AttractionDetailAPIView,
    CommentListCreateAPIView,
    CommentDetailAPIView,
    AttractionCommentListAPIView
)

urlpatterns = [
    path('attractions/', AttractionListCreateAPIView.as_view(), name='attraction-list-create'),
    path('attractions/<int:pk>/', AttractionDetailAPIView.as_view(), name='attraction-detail'),
    path('attractions/<int:attraction_id>/comments/', AttractionCommentListAPIView.as_view(), name='attraction-comments'),
    path('comments/', CommentListCreateAPIView.as_view(), name='comment-list-create'),
    path('comments/<int:pk>/', CommentDetailAPIView.as_view(), name='comment-detail'),
]
