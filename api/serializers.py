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


class ProductIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["pk", ]


class CouponIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = ["pk", ]


class CustomerSubscriptionIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerSubscription
        fields = ["pk", ]


class ManageSubscriptionSerializer(serializers.Serializer):
    product = serializers.IntegerField()
    subscription = serializers.IntegerField()

    def validate_product(self, obj_id):
        obj = None
        try:
            obj = Product.objects.get(pk=obj_id)
        except Product.DoesNotExist:
            raise serializers.ValidationError()
        return obj

    def validate_subscription(self, obj_id):
        obj = None
        try:
            obj = CustomerSubscription.objects.get(pk=obj_id)
        except CustomerSubscription.DoesNotExist:
            raise serializers.ValidationError()
        return obj


class CouponProductSerializer(serializers.Serializer):
    coupon = serializers.IntegerField()
    product = serializers.IntegerField()

    def validate_product(self, obj_id):
        obj = None
        try:
            obj = Product.objects.get(pk=obj_id)
        except Product.DoesNotExist:
            raise serializers.ValidationError()
        return obj

    def validate_coupon(self, obj_id):
        obj = None
        try:
            obj = Coupon.objects.get(pk=obj_id)
        except Coupon.DoesNotExist:
            raise serializers.ValidationError()
        return obj


class ApplyCouponSerializer(serializers.Serializer):
    items = CouponProductSerializer(many=True)
    subscription = serializers.IntegerField()

    def validate_subscription(self, obj_id):
        obj = None
        try:
            obj = CustomerSubscription.objects.get(pk=obj_id)
        except CustomerSubscription.DoesNotExist:
            raise serializers.ValidationError()
        return obj
