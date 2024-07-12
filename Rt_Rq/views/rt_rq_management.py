from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from ..models import Rt_Rq
from ..serializers import Rt_RqSerializer


class Rt_RqListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        rt_rqs = Rt_Rq.objects.all()
        serializer = Rt_RqSerializer(rt_rqs, many=True)
        return Response(serializer.data)

    def post(self, request):
        if request.user.tourist.user_type != 'admin' and request.user.tourist.user_type != 'agent':
            return Response({"error": "Only administrators and agents can add."}, status=status.HTTP_403_FORBIDDEN)

        serializer = Rt_RqSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Rt_RqDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Rt_Rq.objects.get(pk=pk)
        except Rt_Rq.DoesNotExist:
            return None

    def get(self, request, pk):
        rt_rq = self.get_object(pk)
        if rt_rq is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = Rt_RqSerializer(rt_rq)
        return Response(serializer.data)

    def put(self, request, pk):
        if request.user.tourist.user_type != 'admin' and request.user.tourist.user_type != 'agent':
            return Response({"error": "Only administrators and agents can update."}, status=status.HTTP_403_FORBIDDEN)

        rt_rq = self.get_object(pk)
        if rt_rq is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = Rt_RqSerializer(rt_rq, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        if request.user.tourist.user_type != 'admin' and request.user.tourist.user_type != 'agent':
            return Response({"error": "Only administrators and agents can delete."}, status=status.HTTP_403_FORBIDDEN)

        rt_rq = self.get_object(pk)
        if rt_rq is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        rt_rq.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
