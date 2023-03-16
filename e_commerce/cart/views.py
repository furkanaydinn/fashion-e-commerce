from django.shortcuts import get_object_or_404
from .serializers import CartSerializer,OrderSerializer,OrderProductSerializer
from .models import Cart,Order,OrderProduct
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# Create your views here.

class ShopCartView(APIView):
    permission_classes = [IsAuthenticated]

    @method_decorator(login_required)
    def get(self, request):
        user = request.user
        cart_items = Cart.objects.filter(user=user)
        serializer = CartSerializer(cart_items, many=True)
        
        # calculate total cart price
        total_price = 0
        for item in cart_items:
            total_price += item.product.price * item.quantity
        
        response_data = {
            'cart_items': serializer.data,
            'cart_total': total_price,
        }
        
        return Response(response_data)
    
    @method_decorator(login_required)
    def post(self, request):
        user = request.user
        data = request.data
        serializer = CartSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        product_id = serializer.validated_data['product_id']
        quantity = serializer.validated_data.get('quantity', 1)

        cart_item = Cart.objects.filter(user=user, product_id=product_id).first()
        if cart_item:
            cart_item.quantity += quantity
            cart_item.save()
        else:
            Cart.objects.create(user=user, product_id=product_id, quantity=quantity)

        return Response({'status': 'Product added to cart'}, status=201)

    @method_decorator(login_required)
    def put(self, request, pk):
        user = request.user
        cart_item = get_object_or_404(Cart, pk=pk, user=user)
        serializer = CartSerializer(cart_item, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @method_decorator(login_required)
    def delete(self, request, pk):
        user = request.user
        cart_item = get_object_or_404(Cart, pk=pk, user=user)
        cart_item.delete()
        return Response({'status': 'Product removed from cart'}, status=204)


class OrderView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        orders = Order.objects.filter(user=user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        user = request.user
        cart_items = Cart.objects.filter(user=user)
        total_price = 0
        for cart_item in cart_items:
            total_price += cart_item.quantity * cart_item.product.price
        order_data = {
            'user': user.id,
            'total_price': total_price,
        }
        serializer = OrderSerializer(data=order_data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()

        for cart_item in cart_items:
            order_product_data = {
                'order': order.id,
                'product': cart_item.product.id,
                'quantity': cart_item.quantity,
                'price': cart_item.product.price,
            }
            order_product_serializer = OrderProductSerializer(data=order_product_data)
            order_product_serializer.is_valid(raise_exception=True)
            order_product_serializer.save()

        Cart.objects.filter(user=user).delete()
        return Response({'status': 'Order placed successfully', 'order_code': order.order_code}, status=status.HTTP_201_CREATED)