from rest_framework import serializers

from api.models import Product, Coupon, ProductCoupon, CustomerSubscription


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = "__all__"


class ProductCouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCoupon
        fields = "__all__"


class ProductCouponDetailSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    coupon = CouponSerializer()

    class Meta:
        model = ProductCoupon
        fields = "__all__"


class CustomerSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerSubscription
        fields = "__all__"


class CustomerSubscriptionDetailSerializer(serializers.ModelSerializer):
    products = ProductCouponDetailSerializer(read_only=True, many=True)

    class Meta:
        model = CustomerSubscription
        fields = "__all__"
