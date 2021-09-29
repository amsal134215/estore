from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from api.models import CustomerSubscription, ProductCoupon
from api.serializers import CustomerSubscriptionDetailSerializer, ManageSubscriptionSerializer, ApplyCouponSerializer


class CustomerSubscriptionViewset(ReadOnlyModelViewSet):
    # permission_classes = [IsAuthenticated]
    serializer_class = CustomerSubscriptionDetailSerializer
    queryset = CustomerSubscription.objects.all()


class CustomerSubscriptionCustomViewSet(viewsets.ViewSet):
    @swagger_auto_schema(
        method="post",
        request_body=ManageSubscriptionSerializer(),
    )
    @action(
        detail=False,
        methods=["post"],
    )
    def add_to_subscription(self, request):

        serializer = ManageSubscriptionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        subscription = serializer.validated_data["subscription"]
        prod_coupon = ProductCoupon.objects.create(product=serializer.validated_data["product"])
        subscription.products.add(prod_coupon)

        return Response(status=200, data=CustomerSubscriptionDetailSerializer(subscription).data)

    @swagger_auto_schema(
        method="post",
        request_body=ManageSubscriptionSerializer(),
    )
    @action(
        detail=False,
        methods=["post"],
    )
    def remove_from_subscription(self, request):

        serializer = ManageSubscriptionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        subscription = serializer.validated_data["subscription"]
        for pc in subscription.products.all():
            if pc.product.id == serializer.validated_data["product"].id:
                subscription.products.remove(pc)

        return Response(status=200, data=CustomerSubscriptionDetailSerializer(subscription).data)

    @swagger_auto_schema(
        method="post",
        request_body=ApplyCouponSerializer(),
    )
    @action(
        detail=False,
        methods=["post"],
    )
    def apply_coupons(self, request):

        serializer = ApplyCouponSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        subscription = serializer.validated_data["subscription"]
        items = serializer.validated_data["items"]

        for item in items:
            for pc in subscription.products.all():
                if pc.product.id == item['product'].id:
                    pc.coupon = item['coupon']
                    pc.save()

        sum = 0
        count = 0
        for pc in subscription.products.all():
            if pc.coupon:
                sum += pc.coupon.discount
                count += 1

        if count:
            subscription.global_disc_percent = sum / count
            subscription.save()

        return Response(status=200, data=CustomerSubscriptionDetailSerializer(subscription).data)
