from django.urls import path
from .views import Rt_AtListCreateAPIView, Rt_AtDetailAPIView

urlpatterns = [
    path('rt_at/', Rt_AtListCreateAPIView.as_view(), name='rt_at-list-create'),
    path('rt_at/<int:pk>/', Rt_AtDetailAPIView.as_view(), name='rt_at-detail'),
]
