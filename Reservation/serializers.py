from rest_framework import serializers
from .models import Reservation, Rt_Rq


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['id', 'rv_date', 'tr_id', 'rt_rq_id', 'status']

    def create(self, validated_data):
        return Reservation.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.rv_date = validated_data.get('rv_date', instance.rv_date)
        instance.tr_id = validated_data.get('tr_id', instance.tr_id)
        instance.rt_rq_id = validated_data.get('rt_rq_id', instance.rt_rq_id)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance

    def validate_rt_rq_id(self, value):  # 预约是否有效
        route_reservation = Rt_Rq.objects.get(pk=value.pk)
        current_bookings_count = Reservation.objects.filter(rt_rq_id=value.pk).count()
        if current_bookings_count >= route_reservation.limit:
            raise serializers.ValidationError("This route reservation is already full.")
        return value
