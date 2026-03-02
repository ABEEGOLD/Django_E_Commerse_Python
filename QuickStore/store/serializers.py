from decimal import Decimal
from rest_framework import serializers
from django.db import transaction
from .models import Product, Review, Cart, CartItem, Order, OrderItem


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','title','description','price','discounted_price']
    discounted_price = serializers.SerializerMethodField(method_name='get_discount')


    def get_discount(self, obj: Product):
        return obj.price - (obj.price * Decimal(0.10))


class SimpleProductSerializer(serializers.ModelSerializer):
        class Meta:
            model = Product
            fields = ['id','title','price']



class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id','name','review','product']

    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(
            product_id = product_id,
            **validated_data
        )


class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField(method_name='get_total_price')


    class Meta:
        model = CartItem
        fields = ['id', 'product','quantity','total_price']

    def get_total_price(self,item: CartItem):
        return item.quantity * item.product.price



class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True,read_only=True)
    total_price = serializers.SerializerMethodField(method_name='get_total_price')

    def get_total_price(self,cart: Cart):
        return sum([item.quantity * item.product.price for item in cart.items.all()])

    class Meta:
         model = Cart
         fields = ['cart_id','items','total_price']

class AddCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id','product','quantity']

    def validate_product(self, product):
        if Product.objects.filter(id=product).exists():
            raise serializers.ValidationError("Product already exists")
        return product


    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product = self.validated_data['product']
        quantity = self.validated_data['quantity']


        try:
           cart_item =  CartItem.objects.get(cart_id=cart_id,product_id=product)
           cart_item.quantity += quantity
           cart_item.save()
           self.instance = cart_item
        except CartItem.DoesNotExist:
            CartItem.objects.create(cart_id=cart_id, **self.validated_data)


        return self.instance


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']


class OrderItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    class Meta:
        model = OrderItem
        fields = ['order', 'product', 'quantity', 'unit_price']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True,read_only=True)
    class Meta:
        model = Order
        fields = ['user', 'items']


class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()

    def validate_cart_id(self, cart_id):
        if not Cart.objects.filter(cart_id=cart_id).exists():
            raise serializers.ValidationError("Cart's does not exist")
        if CartItem.objects.filter(cart_id=cart_id).count() == 0:
            raise serializers.ValidationError("Cannot place order for empty cart")
        return cart_id


    def save(self, **kwargs):
        with transaction.atomic():
            cart_id = self.validated_data['cart_id']
            user_id = self.context['user_id']


            order = Order.objects.create(user_id=user_id)

            cart_items = CartItem.objects.filter(cart_id=cart_id)


            order_items =[
                OrderItem(
                     order = order,
                     product=item.product,
                     quantity=item.quantity,
                     unit_price=item.product.price
                )for item in cart_items
            ]

            OrderItem.objects.bulk_create(order_items)

            Cart.objects.filter(cart_id=cart_id).delete()

        return order
