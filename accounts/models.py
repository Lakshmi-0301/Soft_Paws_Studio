from django.db import models
from django.contrib.auth.models import User


class Products(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=255)
    color = models.CharField(max_length=50)
    size = models.CharField(max_length=50)
    availability = models.IntegerField()
    mrp = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100)
    image = models.CharField(max_length=500)  
    brand = models.CharField(max_length=100)
    stock = models.IntegerField()
    material = models.CharField(max_length=100)

    def __str__(self):
        return self.product_name
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def get_total_price(self):
        return self.product.mrp * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.product_name}"
    
    
class CustomerInfo(models.Model):
    customerid = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    apartment_number = models.CharField(max_length=255)
    street_name = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    pincode = models.CharField(max_length=20)
    payment_mode = models.CharField(max_length=50, choices=[("cash", "Cash"), ("card", "Card"), ("net_banking", "Net Banking")])

    def __str__(self):
        return self.customerid.username
    
class OrderHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey('Products', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.quantity})"
    
class ProductReview(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)  
    product = models.ForeignKey('Products', related_name='reviews', on_delete=models.CASCADE)  # Add related_name
    rating = models.PositiveSmallIntegerField()  
    review_text = models.TextField(null=True, blank=True)  
    created_at = models.DateTimeField(auto_now_add=True)  
    
    def __str__(self):
            return f"Review by {self.customer.username} for {self.product.product_name}"