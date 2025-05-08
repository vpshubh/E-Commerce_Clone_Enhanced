
# orders/views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer
from cart.models import Cart

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        # Get active cart
        try:
            cart = Cart.objects.get(user=request.user, completed=False)
        except Cart.DoesNotExist:
            return Response(
                {'error': 'No active cart found'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Ensure cart has items
        if not cart.items.exists():
            return Response(
                {'error': 'Your cart is empty'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create order
        order_data = {
            'user': request.user,
            'full_name': request.data.get('full_name'),
            'email': request.data.get('email'),
            'address': request.data.get('address'),
            'phone': request.data.get('phone'),
            'total_amount': cart.total_price,
        }
        
        order = Order.objects.create(**order_data)
        
        # Create order items from cart items
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                price=cart_item.product.discount_price or cart_item.product.price,
                quantity=cart_item.quantity
            )
        
        # Mark cart as completed
        cart.completed = True
        cart.save()
        
        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

