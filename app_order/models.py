from django.db import models
from django.conf import settings
from app_shop.models import Product
# from Multi_Vendor.models import VendorProduct
# Create your models here.


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name="cart")
    item = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="cart_product")

    quantity = models.IntegerField(default=1)
    purchased = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.quantity} X {self.item}"

    def get_total(self):
        return format(self.item.price * self.quantity, "0.2f")


class Order(models.Model):
    orderItems = models.ManyToManyField(Cart)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    paymentId = models.CharField(max_length=564, blank=True, null=True)
    orderId = models.CharField(max_length=500, blank=True, null=True)
    card_type = models.CharField(max_length=200, blank=True, null=True)

    def get_totals(self):
        total = 0
        for order_item in self.orderItems.all():
            total += float(order_item.get_total())
        return total

    def __str__(self) -> str:
        return str(self.user)
