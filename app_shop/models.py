from django.db import models
from django.conf import settings
# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name_plural = "Categories"


class Shops(models.Model):
    shop_name = models.CharField(max_length=200)
    address = models.CharField(max_length=256, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.shop_name


class Product(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    shops = models.ForeignKey(
        Shops, on_delete=models.CASCADE, related_name="product_shop")
    coupon_code = models.CharField(max_length=50, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="product_category")
    image = models.ImageField(upload_to="vendorImage")
    name = models.CharField(max_length=264)
    description = models.TextField(
        max_length=1000, verbose_name="Description")
    price = models.FloatField()
    old_price = models.FloatField(null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ["-created",]
