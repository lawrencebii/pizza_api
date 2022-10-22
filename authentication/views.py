from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
# Create your views here.
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from authentication import serialization
from .models import User


# class HelloAuthView(generics.GenericAPIView):
#     def get(self, request):
#         return Response(data={'message': 'Hello Lawrence bii'}, status=status.HTTP_200_OK)


class UserCreateView(generics.GenericAPIView):
    serializer_class = serialization.UserCreationSerializer

    @swagger_auto_schema(operation_summary="Create a user account")
    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AllUsersView(generics.GenericAPIView):
    serializer_class = serialization.UserCreationSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    @swagger_auto_schema(operation_summary="List all users")
    def get(self, request):
        data = User.objects.all()
        serial = self.serializer_class(instance=data, many=True)
        return Response(data=serial.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_summary="Delete user")
    def delete(self, user_id):
        user = get_object_or_404(User, pk=user_id)
        user.delete()
