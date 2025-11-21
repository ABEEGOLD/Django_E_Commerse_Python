import uuid

from django.db import models
from django.conf import settings

# Create your models here.

class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    updated_at = models.DateTimeField(auto_now=True)
    inventory = models.PositiveIntegerField()
    collection = models.ForeignKey('Collection', on_delete=models.CASCADE,related_name='products')

    def __str__(self):
        return self.title


class Collection(models.Model):
    title = models.CharField(max_length=100)
    # Product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Cart(models.Model):
    cart_id = models.UUIDField(default=uuid.uuid4, editable=False,primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE,related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()


    class Meta:
        unique_together = ['cart','product']


class Order(models.Model):
    ORDER_STATUS = (
        ('P','Pending'),
        ('C','Completed'),
        ('F','Failed'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,related_name='user_order')
    placed_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1, choices=ORDER_STATUS, default='P')
    cart = models.ForeignKey(Cart, on_delete=models.PROTECT)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)


class Review(models.Model):
    name = models.CharField(max_length=100)
    review = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)






