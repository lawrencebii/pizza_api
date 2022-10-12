from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
# Create your views here.
from rest_framework.response import Response

from authentication import serialization


class HelloAuthView(generics.GenericAPIView):
    def get(self, request):
        return Response(data={'message': 'Hello Lawrence bii'}, status=status.HTTP_200_OK)


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
