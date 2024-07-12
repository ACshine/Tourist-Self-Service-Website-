from django.urls import path
from .views import Rt_RqListCreateAPIView, Rt_RqDetailAPIView

urlpatterns = [
    path('rt_rq/', Rt_RqListCreateAPIView.as_view(), name='rt_rq_list_create'),
    path('rt_rq/<int:pk>/', Rt_RqDetailAPIView.as_view(), name='rt_rq_detail'),
]
