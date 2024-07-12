from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from ..models import Route
from ..serializers import RouteSerializer


class RouteListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        routes = Route.objects.all()
        serializer = RouteSerializer(routes, many=True)
        return Response(serializer.data)

    def post(self, request):
        if request.user.tourist.user_type != 'admin' and request.user.tourist.user_type != 'agent':
            return Response({"error": "Only administrators and agents can add routes."}, status=status.HTTP_403_FORBIDDEN)

        serializer = RouteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RouteDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Route.objects.get(pk=pk)
        except Route.DoesNotExist:
            return None

    def get(self, request, pk):
        route = self.get_object(pk)
        if route is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = RouteSerializer(route)
        return Response(serializer.data)

    def put(self, request, pk):
        if request.user.tourist.user_type != 'admin' and request.user.tourist.user_type != 'agent':
            return Response({"error": "Only administrators and agents can update routes."}, status=status.HTTP_403_FORBIDDEN)

        route = self.get_object(pk)
        if route is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = RouteSerializer(route, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        if request.user.tourist.user_type != 'admin' and request.user.tourist.user_type != 'agent':
            return Response({"error": "Only administrators and agents can delete routes."}, status=status.HTTP_403_FORBIDDEN)

        route = self.get_object(pk)
        if route is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        route.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
