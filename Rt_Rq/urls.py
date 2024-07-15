from django.urls import path
from .views import Rt_RqListCreateAPIView, Rt_RqDetailAPIView, Rt_RqDatesAPIView, Rt_RqRoutesAPIView


urlpatterns = [
    path('rt_rq/', Rt_RqListCreateAPIView.as_view(), name='rt_rq_list_create'),
    path('rt_rq/<int:pk>/', Rt_RqDetailAPIView.as_view(), name='rt_rq_detail'),
    path('rt_rq/route/<int:route_id>/', Rt_RqDatesAPIView.as_view(), name='rt_rq-route-dates'),
    path('rt_rq/date/<str:date>/', Rt_RqRoutesAPIView.as_view(), name='rt_rq-date-routes'),
]
