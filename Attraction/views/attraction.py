from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from ..models import Attraction, Comment, AttractionImage, CommentImage
from ..serializers import AttractionSerializer, CommentSerializer, AttractionImageSerializer, CommentImageSerializer

class AttractionCommentListAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, attraction_id):
        comments = Comment.objects.filter(attraction_id=attraction_id)
        serializer = CommentSerializer(comments, many=True, context={'request': request})
        return Response(serializer.data)


class AttractionListCreateAPIView(APIView):

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request):
        attractions = Attraction.objects.all()
        serializer = AttractionSerializer(attractions, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        if request.user.tourist.user_type != 'admin':
            return Response({"error": "Only administrators can add attractions."}, status=status.HTTP_403_FORBIDDEN)

        name = request.data.get('name')
        address = request.data.get('address')
        if Attraction.objects.filter(name=name, address=address).exists():
            return Response({"error": "Attraction with this name and address already exists."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = AttractionSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            attraction = serializer.save()
            images = request.FILES.getlist('images')
            for image in images:
                AttractionImage.objects.create(attraction=attraction, image=image)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AttractionDetailAPIView(APIView):

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_object(self, pk):
        try:
            return Attraction.objects.get(pk=pk)
        except Attraction.DoesNotExist:
            return None

    def get(self, request, pk):
        attraction = self.get_object(pk)
        if attraction is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # 增加搜索次数并更新热度
        attraction.search_count += 1
        attraction.update_popularity()

        serializer = AttractionSerializer(attraction, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        if request.user.tourist.user_type != 'admin':
            return Response({"error": "Only administrators can update attractions."}, status=status.HTTP_403_FORBIDDEN)

        attraction = self.get_object(pk)
        if attraction is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = AttractionSerializer(attraction, data=request.data, context={'request': request})
        if serializer.is_valid():
            attraction = serializer.save()
            images = request.FILES.getlist('images')
            for image in images:
                AttractionImage.objects.create(attraction=attraction, image=image)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        if request.user.tourist.user_type != 'admin':
            return Response({"error": "Only administrators can delete attractions."}, status=status.HTTP_403_FORBIDDEN)

        attraction = self.get_object(pk)
        if attraction is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        attraction.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


