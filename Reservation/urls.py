from django.urls import path
from .views import ReservationListCreateAPIView, ReservationDetailAPIView

urlpatterns = [
    path('reservations/', ReservationListCreateAPIView.as_view(), name='reservation-list-create'),
    path('reservations/<int:pk>/', ReservationDetailAPIView.as_view(), name='reservation-detail'),
]
