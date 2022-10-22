from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
# Create your views here.
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from . import serializer
from .models import Order, User
from .serializer import StatusUpdateSerializer

User = get_user_model()


class HelloAuthView(generics.GenericAPIView):
    def get(self, request):
        return Response(data={'message': 'Made by Lawrence bii'}, status=status.HTTP_200_OK)


# ORDERS
class OrderCreateListView(generics.GenericAPIView):
    serializer_class = serializer.OrderSerializer
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(operation_summary="List all orders")
    def get(self, request):
        isAdmin = request.user.is_superuser
        forders = Order.objects.all().filter(customer=request.user)
        allOrders = Order.objects.all()
        serializer = self.serializer_class(instance=allOrders if isAdmin else forders, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_summary="Create a new order")
    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        user = request.user
        if serializer.is_valid():
            serializer.save(customer=user)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Order details
class OrderDetailView(generics.GenericAPIView):
    serializer_class = serializer.OrderDetailSerializer
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(operation_summary="Get a particular order by id")
    def get(self, request, order_id):
        order = get_object_or_404(Order, pk=order_id)
        serial = self.serializer_class(instance=order)
        return Response(data=serial.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_summary="Update an order by id")
    def put(self, request, order_id):
        # user = request.user
        data = request.data
        order = get_object_or_404(Order, pk=order_id)
        serial = self.serializer_class(data=data, instance=order)
        if serial.is_valid():
            serial.save()
            return Response(data=serial.data, status=status.HTTP_200_OK)
        return Response(data=serial.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_summary="Remove an Order")
    def delete(self, request, order_id):
        order = get_object_or_404(Order, pk=order_id)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT, data={'message': 'Order deleted successfully'})


'''serial = self.serializer_class(data=data)
        if serial.is_valid():
            serializer.save(customer=user)
            return Response(data=serial.data, status=status.HTTP_200_OK)
        return Response(data=serial.errors, status=status.HTTP_400_BAD_REQUEST)'''


class UpdateOrderStatus(generics.GenericAPIView):
    serializer_class = StatusUpdateSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(operation_summary="Update an order status")
    def put(self, request, order_id):
        order = get_object_or_404(Order, pk=order_id)
        data = request.data
        serial = self.serializer_class(data=data, instance=order)
        if serial.is_valid():
            serial.save()
            return Response(data=serial.data, status=status.HTTP_200_OK)
        return Response(data=serial.errors, status=status.HTTP_400_BAD_REQUEST)


class UserOrdersView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = serializer.OrderDetailSerializer
    queryset = Order

    @swagger_auto_schema(operation_summary="Get all orders for a particular user by id")
    def get(self, request, user_id):
        # user = request.user
        user = User.objects.get(pk=user_id)
        orders = Order.objects.all().filter(customer=user)
        serial = self.serializer_class(instance=orders, many=True)

        return Response(data=serial.data, status=status.HTTP_200_OK)


class UserOrderDetail(generics.GenericAPIView):
    serializer_class = serializer.OrderSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(operation_summary="Get a user's order by user_id and order id")
    def get(self, request, user_id, order_id):
        user = User.objects.get(pk=user_id)
        # orders = Order.objects.get(customer=user).get(pk=order_id)
        orders = Order.objects.all().filter(customer=user).get(pk=order_id)
        serial = self.serializer_class(instance=orders)
        return Response(data=serial.data, status=status.HTTP_200_OK)
