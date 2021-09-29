from django.contrib.auth.models import AbstractUser
from django.db import models

from api.models import CustomerSubscription


class Customer(AbstractUser):
    subscription = models.OneToOneField(CustomerSubscription, null=True, blank=True,
                                        on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Customer"
