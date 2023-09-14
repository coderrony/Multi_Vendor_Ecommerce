from django.db import models
from django.conf import settings
from app_shop.models import Product
from app_order.models import Order
# Create your models here.


class BillingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    address = models.CharField(max_length=264, blank=True)
    zipcode = models.CharField(max_length=10, blank=True)
    city = models.CharField(max_length=30, blank=True)
    country = models.CharField(max_length=30, blank=True)

    def __str__(self) -> str:
        return f"{self.user.profile.username} billing address"

    def is_fully_filled(self):
        fields_names = [f.name for f in self._meta.get_field()]

        for field_name in fields_names:

            value = getattr(self, field_name)
            if value is None or value == "":
                return False
        return True

    class Meta:
        verbose_name_plural = "Billing Addresses"


# class CompleteOrder(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL,
#                              on_delete=models.CASCADE, related_name="completeOrderUser")
#     orderProduct = models.ForeignKey(
#         Product, on_delete=models.CASCADE, related_name="completeOrderProduct")
#     orderHistory = models.ForeignKey(
#         Order, models.CASCADE, related_name="completeOrderHistory")
#     created = models.DateTimeField(auto_now_add=True)

#     def __str__(self) -> str:
#         return str(self.user)
