from decimal import Decimal
from rest_framework import serializers
from .models import Product, Review, Cart, CartItem


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','title','description','price','discounted_price']
    discounted_price = serializers.SerializerMethodField(method_name='get_discount')


    def get_discount(self, obj: Product):
        return obj.price - (obj.price * Decimal(0.10))

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id','name','review']

    def create(self, validated_data):
        product_id = validated_data['product_id']
        return Review.objects.create(
            product_id = product_id,
            **validated_data
        )


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    total_price = serializers.SerializerMethodField(method_name='get_total_price')


    class Meta:
        model = CartItem
        fields = ['id','product','quantity','total_price']

    def get_total_price(self,item: CartItem):
        return item.product.price * item.quantity



class cartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True,read_only=True)
    total_price = serializers.SerializerMethodField(method_name='get_total_price')

    def get_total_price(self,cart: CartItem):
        return sum([item.product.price * item.quantity for item in cart.items.all()])

    class Meta:
         model = Cart
         fields = ['cart_id','items','total_price']