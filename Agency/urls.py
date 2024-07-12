from django.urls import path
from . import views
from .views import AgencyListCreateAPIView, AgencyDetailAPIView

urlpatterns = [
    path('agencies/', AgencyListCreateAPIView.as_view(), name='agency-list-create'),
    path('agencies/<int:pk>/', AgencyDetailAPIView.as_view(), name='agency-detail'),
]
