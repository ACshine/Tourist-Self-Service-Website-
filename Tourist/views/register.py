from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from ..models import Tourist
from ..serializers import TouristSerializer
from rest_framework.authtoken.models import Token

class RegisterAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user_type = request.data.get('user_type')
        if user_type not in ['regular', 'vip', 'agent']:
            return Response({"error": "Invalid user type."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = TouristSerializer(data=request.data)
        if serializer.is_valid():
            tourist = serializer.save()
            token, created = Token.objects.get_or_create(user=tourist.user)
            return Response({"token": token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
