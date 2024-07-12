from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from ..models import Agency
from ..serializers import AgencySerializer


class AgencyListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        agencies = Agency.objects.all()
        serializer = AgencySerializer(agencies, many=True)
        return Response(serializer.data)

    def post(self, request):
        if request.user.tourist.user_type != 'admin':
            return Response({"error": "Only administrators can add agencies."}, status=status.HTTP_403_FORBIDDEN)

        serializer = AgencySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AgencyDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Agency.objects.get(pk=pk)
        except Agency.DoesNotExist:
            return None

    def get(self, request, pk):
        agency = self.get_object(pk)
        if agency is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = AgencySerializer(agency)
        return Response(serializer.data)

    def put(self, request, pk):
        if request.user.tourist.user_type != 'admin':
            return Response({"error": "Only administrators can update agencies."}, status=status.HTTP_403_FORBIDDEN)

        agency = self.get_object(pk)
        if agency is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = AgencySerializer(agency, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        if request.user.tourist.user_type != 'admin':
            return Response({"error": "Only administrators can delete agencies."}, status=status.HTTP_403_FORBIDDEN)

        agency = self.get_object(pk)
        if agency is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        agency.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
