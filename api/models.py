from django.db import models


class Product(models.Model):
    sku = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    price = models.FloatField()


class Coupon(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100)
    discount = models.FloatField()
    expires_at = models.DateTimeField(null=True, blank=True)


class ProductCoupon(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, null=True, blank=True)


class CustomerSubscription(models.Model):
    subscription_code = models.CharField(max_length=100, unique=True)
    products = models.ManyToManyField(ProductCoupon, null=True, blank=True)
    global_disc_percent = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
