from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from ..models import FrequentTraveler, FavoriteAttraction
from ..serializers import TouristSerializer, FrequentTravelerSerializer, FavoriteAttractionSerializer

class UserProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tourist = request.user.tourist
        serializer = TouristSerializer(tourist)
        return Response(serializer.data)

    def put(self, request):
        tourist = request.user.tourist
        serializer = TouristSerializer(tourist, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FrequentTravelerListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        travelers = FrequentTraveler.objects.filter(user=request.user.tourist)
        serializer = FrequentTravelerSerializer(travelers, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = FrequentTravelerSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FrequentTravelerDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return FrequentTraveler.objects.get(pk=pk, user=self.request.user.tourist)
        except FrequentTraveler.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        traveler = self.get_object(pk)
        if isinstance(traveler, Response):
            return traveler
        serializer = FrequentTravelerSerializer(traveler)
        return Response(serializer.data)

    def put(self, request, pk):
        traveler = self.get_object(pk)
        if isinstance(traveler, Response):
            return traveler
        serializer = FrequentTravelerSerializer(traveler, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        traveler = self.get_object(pk)
        if isinstance(traveler, Response):
            return traveler
        traveler.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class FavoriteAttractionListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        favorites = FavoriteAttraction.objects.filter(user=request.user.tourist)
        serializer = FavoriteAttractionSerializer(favorites, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = FavoriteAttractionSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FavoriteAttractionDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, attraction_id):
        try:
            favorite = FavoriteAttraction.objects.get(attraction_id=attraction_id, user=request.user.tourist)
        except FavoriteAttraction.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)