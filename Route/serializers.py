from rest_framework import serializers
from .models import Route


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ['id', 'rt_name', 'ag_id', 'price', 'rt_brief']

    def create(self, validated_data):
        return Route.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.rt_name = validated_data.get('rt_name', instance.rt_name)
        instance.ag_id = validated_data.get('ag_id', instance.ag_id)
        instance.price = validated_data.get('price', instance.price)
        instance.rt_brief = validated_data.get('rt_brief', instance.rt_brief)
        instance.save()
        return instance
