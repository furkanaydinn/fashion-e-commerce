from rest_framework import serializers
from .models import Cart, Order,OrderProduct

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    cart = CartSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = '__all__'

class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = '__all__'

