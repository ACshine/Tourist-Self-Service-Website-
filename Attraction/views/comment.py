from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from ..models import Attraction, Comment, CommentImage
from ..serializers import AttractionSerializer, CommentSerializer, AttractionImageSerializer, CommentImageSerializer

class CommentListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            comment = serializer.save(user=request.user.tourist)
            images = request.FILES.getlist('images')
            for image in images:
                CommentImage.objects.create(comment=comment, image=image)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        comment = self.get_object(pk)
        if isinstance(comment, Response):
            return comment
        serializer = CommentSerializer(comment, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        comment = self.get_object(pk)
        if isinstance(comment, Response):
            return comment

        # 检查用户权限
        if comment.user != request.user.tourist and request.user.tourist.user_type != 'admin':
            return Response({"error": "You do not have permission to edit this comment."}, status=status.HTTP_403_FORBIDDEN)

        # 如果包含 'is_featured' 字段，检查是否为管理员
        if 'is_featured' in request.data and request.user.tourist.user_type != 'admin':
            return Response({"error": "Only administrators can set featured comments."}, status=status.HTTP_403_FORBIDDEN)

        serializer = CommentSerializer(comment, data=request.data, context={'request': request})
        if serializer.is_valid():
            comment = serializer.save(user=request.user.tourist)
            images = request.FILES.getlist('images')
            for image in images:
                CommentImage.objects.create(comment=comment, image=image)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        comment = self.get_object(pk)
        if isinstance(comment, Response):
            return comment

        # 检查用户权限
        if comment.user != request.user.tourist and request.user.tourist.user_type != 'admin':
            return Response({"error": "You do not have permission to delete this comment."}, status=status.HTTP_403_FORBIDDEN)

        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
