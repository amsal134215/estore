from django.contrib import admin

from api.models import Product, Coupon, ProductCoupon, CustomerSubscription

admin.site.register(Product)
admin.site.register(Coupon)
admin.site.register(ProductCoupon)
admin.site.register(CustomerSubscription)
