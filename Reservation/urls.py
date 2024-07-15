from django.urls import path
from .views import ReservationListCreateAPIView, ReservationDetailAPIView, ReservationsByDateAPIView
from .views import ReservationsByTouristAPIView, ReservationsByRouteAPIView
urlpatterns = [
    path('reservations/', ReservationListCreateAPIView.as_view(), name='reservation-list-create'),
    path('reservations/<int:pk>/', ReservationDetailAPIView.as_view(), name='reservation-detail'),
    path('reservations/date/<str:date>/', ReservationsByDateAPIView.as_view(), name='reservations-by-date'),
    path('reservations/tourist/<int:tr_id>/', ReservationsByTouristAPIView.as_view(), name='reservations-by-tourist'),
    path('reservations/route/<int:rt_rq_id>/', ReservationsByRouteAPIView.as_view(), name='reservations-by-route'),
]
