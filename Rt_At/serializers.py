from rest_framework import serializers
from .models import Rt_At


class Rt_AtSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rt_At
        fields = ['id', 'rt_id', 'at_id']

    def create(self, validated_data):
        return Rt_At.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.rt_id = validated_data.get('rt_id', instance.rt_id)
        instance.at_id = validated_data.get('at_id', instance.at_id)
        instance.save()
        return instance
