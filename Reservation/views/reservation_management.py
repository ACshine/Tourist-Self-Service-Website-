from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Rt_Rq.models import Rt_Rq
from ..models import Reservation
from ..serializers import ReservationSerializer


class ReservationListCreateAPIView(APIView):

    def get(self, request):
        reservations = Reservation.objects.all()
        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ReservationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReservationsByDateAPIView(APIView):

    def get(self, request, date):
        reservations = Reservation.objects.filter(rv_date=date)
        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data)


class ReservationsByTouristAPIView(APIView):

    def get(self, request, tr_id):
        reservations = Reservation.objects.filter(tr_id=tr_id)
        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data)


class ReservationsByRouteAPIView(APIView):

    def get(self, request, rt_rq_id):
        rt_rqs = Rt_Rq.objects.filter(pk=rt_rq_id)
        reservation_ids = [rt_rq.id for rt_rq in rt_rqs]
        reservations = Reservation.objects.filter(rt_rq_id__in=reservation_ids)
        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data)


class ReservationDetailAPIView(APIView):

    def get_object(self, pk):
        try:
            return Reservation.objects.get(pk=pk)
        except Reservation.DoesNotExist:
            return None

    def get(self, request, pk):
        reservation = self.get_object(pk)
        if reservation is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ReservationSerializer(reservation)
        return Response(serializer.data)

    def put(self, request, pk):
        reservation = self.get_object(pk)
        if reservation is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ReservationSerializer(reservation, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        reservation = self.get_object(pk)
        if reservation is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        reservation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
