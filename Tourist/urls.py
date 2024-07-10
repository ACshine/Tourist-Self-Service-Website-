from django.urls import path
from .views import RegisterAPIView, LoginAPIView, UserProfileAPIView, FrequentTravelerListCreateAPIView, FrequentTravelerDetailAPIView, FavoriteAttractionListCreateAPIView, FavoriteAttractionDetailAPIView

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('profile/', UserProfileAPIView.as_view(), name='profile'),
    path('frequent_travelers/', FrequentTravelerListCreateAPIView.as_view(), name='frequent_travelers'),
    path('frequent_travelers/<int:pk>/', FrequentTravelerDetailAPIView.as_view(), name='frequent_traveler_detail'),
    path('favorites/', FavoriteAttractionListCreateAPIView.as_view(), name='favorites'),
    path('favorites/<int:attraction_id>/', FavoriteAttractionDetailAPIView.as_view(), name='favorite_detail'),
]
