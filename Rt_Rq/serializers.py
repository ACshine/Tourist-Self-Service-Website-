from rest_framework import serializers
from Reservation.models import Reservation
from .models import Rt_Rq



class Rt_RqSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rt_Rq
        fields = ['id', 'rt_id', 'rq', 'days', 'limit']

    def create(self, validated_data):
        return Rt_Rq.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.rt_id = validated_data.get('rt_id', instance.rt_id)
        instance.rq = validated_data.get('rq', instance.rq)
        instance.days = validated_data.get('days', instance.days)
        instance.limit = validated_data.get('limit', instance.limit)
        instance.save()
        return instance

    def validate_limit(self, value):
        rt_rq_instance = self.instance
        if rt_rq_instance:
            current_bookings_count = Reservation.objects.filter(rt_rq_id=rt_rq_instance.pk).count()
            if value < current_bookings_count:
                raise serializers.ValidationError("New limit cannot be less than current bookings count.")
        return value
