from rest_framework import serializers

from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    size = serializers.CharField(max_length=20, )
    # url = serializers.ImageField()
    order_status = serializers.CharField(max_length=20, default='PENDING')
    quantity = serializers.IntegerField()

    class Meta:
        model = Order
        # fields = ['size', 'order_status', 'quantity', 'order_id']
        fields = '__all__'


class OrderDetailSerializer(serializers.ModelSerializer):
    size = serializers.CharField(max_length=20, )
    # url = serializers.ImageField()
    order_status = serializers.CharField(default='PENDING')
    quantity = serializers.IntegerField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()

    class Meta:
        model = Order
        fields = ['id', 'size', 'order_status', 'quantity', 'created_at', 'updated_at']

        # fields = '__all__'


class StatusUpdateSerializer(serializers.ModelSerializer):
    order_status = serializers.CharField(default='PENDING')

    class Meta:
        model = Order
        fields = ['order_status']
