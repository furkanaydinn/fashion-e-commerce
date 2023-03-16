from django.db import models
from django.contrib.auth.models import User
from shop.models import Product

# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Cart"

class Order(models.Model):
    STATUS_CHOICES = (
        ('P', 'Processing'),
        ('S', 'Shipped'),
        ('D', 'Delivered'),
        ('C', 'Cancelled'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart = models.ManyToManyField(Cart)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    date_ordered = models.DateTimeField(auto_now_add=True)
    order_code = models.CharField(max_length=20, unique=True)
    country = models.CharField(blank=True, max_length=20)
    city = models.CharField(blank=True, max_length=20)
    address = models.CharField(blank=True, max_length=150)
    phone = models.CharField(blank=True, max_length=20)
    zip_code = models.CharField(blank=True, max_length=8)
    adminnote = models.CharField(blank=True, max_length=100)

    def __str__(self):
        return f"{self.user.username}'s Order"
    

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.order.order_code}-{self.product.name}"





