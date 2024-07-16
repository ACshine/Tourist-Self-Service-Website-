from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Tourist, FrequentTraveler, FavoriteAttraction
import re


class UserSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True, required=False)
    password = serializers.CharField(write_only=True, required=False)
    password2 = serializers.CharField(write_only=True, required=False, label="Confirm password")

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'password2', 'old_password', 'first_name', 'last_name', 'email']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_password(self, value):
        if len(value) < 6:
            raise serializers.ValidationError("Password must be at least 6 characters long.")
        if not re.search(r'[A-Za-z]', value) or not re.search(r'[0-9]', value):
            raise serializers.ValidationError("Password must contain both letters and numbers.")
        return value

    def validate(self, data):
        user = self.context['request'].user if 'request' in self.context else None
        if 'password' in data and 'password2' in data:
            if data['password'] != data['password2']:
                raise serializers.ValidationError("Passwords do not match.")
            if 'old_password' in data:
                if not user:
                    raise serializers.ValidationError("User not found.")
                if not user.check_password(data['old_password']):
                    raise serializers.ValidationError("Old password is incorrect.")
                if data['password'] == data['old_password']:
                    raise serializers.ValidationError("New password cannot be the same as the old password.")
        return data

    def create(self, validated_data):
        validated_data.pop('password2', None)
        validated_data.pop('old_password', None)
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data.pop('password'),
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email']
        )
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        validated_data.pop('password2', None)
        validated_data.pop('old_password', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance

class TouristSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    points = serializers.IntegerField(read_only=True)

    class Meta:
        model = Tourist
        fields = ['user', 'avatar', 'user_type', 'points']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        tourist, created = Tourist.objects.update_or_create(user=user, user_type=validated_data.pop('user_type'))
        return tourist

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            user = instance.user
            user_serializer = self.fields['user']
            user_serializer.update(user, user_data)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class FrequentTravelerSerializer(serializers.ModelSerializer):
    class Meta:
        model = FrequentTraveler
        fields = ['id', 'user', 'name', 'phone_number', 'id_type', 'id_number', 'nationality', 'gender']
        read_only_fields = ['user']

    def create(self, validated_data):
        user = self.context['request'].user.tourist
        validated_data['user'] = user
        return super().create(validated_data)

class FavoriteAttractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteAttraction
        fields = ['id', 'user', 'attraction']
        read_only_fields = ['user']

    def create(self, validated_data):
        user = self.context['request'].user.tourist
        validated_data['user'] = user
        return super().create(validated_data)
