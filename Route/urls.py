from django.urls import path
from .views import RouteListCreateAPIView, RouteDetailAPIView

urlpatterns = [
    path('routes/', RouteListCreateAPIView.as_view(), name='route-list-create'),
    path('routes/<int:pk>/', RouteDetailAPIView.as_view(), name='route-detail'),
]
