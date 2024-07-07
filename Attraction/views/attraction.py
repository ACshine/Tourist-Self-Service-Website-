from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from ..models import Attraction
from ..serializers import AttractionSerializer


class AttractionListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        attractions = Attraction.objects.all()
        serializer = AttractionSerializer(attractions, many=True)
        return Response(serializer.data)

    def post(self, request):
        if request.user.tourist.user_type != 'admin':
            return Response({"error": "Only administrators can add attractions."}, status=status.HTTP_403_FORBIDDEN)

        serializer = AttractionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AttractionDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Attraction.objects.get(pk=pk)
        except Attraction.DoesNotExist:
            return None

    def get(self, request, pk):
        attraction = self.get_object(pk)
        if attraction is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = AttractionSerializer(attraction)
        return Response(serializer.data)

    def put(self, request, pk):
        if request.user.tourist.user_type != 'admin':
            return Response({"error": "Only administrators can update attractions."}, status=status.HTTP_403_FORBIDDEN)

        attraction = self.get_object(pk)
        if attraction is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = AttractionSerializer(attraction, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        if request.user.tourist.user_type != 'admin':
            return Response({"error": "Only administrators can delete attractions."}, status=status.HTTP_403_FORBIDDEN)

        attraction = self.get_object(pk)
        if attraction is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        attraction.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
