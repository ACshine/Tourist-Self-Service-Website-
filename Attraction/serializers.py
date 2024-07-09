from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Tourist, Attraction, Comment, AttractionImage, CommentImage
import re

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True, label="Confirm password")

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'password2', 'first_name', 'last_name', 'email']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_password(self, value):
        if len(value) < 6:
            raise serializers.ValidationError("Password must be at least 6 characters long.")
        if not re.search(r'[A-Za-z]', value) or not re.search(r'[0-9]', value):
            raise serializers.ValidationError("Password must contain both letters and numbers.")
        return value

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email']
        )
        return user

class TouristSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Tourist
        fields = ['user', 'avatar', 'user_type']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        tourist, created = Tourist.objects.update_or_create(user=user, user_type=validated_data.pop('user_type'))
        return tourist

class AttractionImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = AttractionImage
        fields = ['id', 'image']

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image and hasattr(obj.image, 'url'):
            return request.build_absolute_uri(obj.image.url)
        return None

class AttractionSerializer(serializers.ModelSerializer):
    images = AttractionImageSerializer(many=True, read_only=True)

    class Meta:
        model = Attraction
        fields = '__all__'

class CommentImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = CommentImage
        fields = ['id', 'image']

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image and hasattr(obj.image, 'url'):
            return request.build_absolute_uri(obj.image.url)
        return None

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    images = CommentImageSerializer(many=True, read_only=True)
    created_at = serializers.ReadOnlyField()

    class Meta:
        model = Comment
        fields = '__all__'
