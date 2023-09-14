from django.contrib import admin
from .models import Category, Shops, Product
# Register your models here.

admin.site.register(Shops)
admin.site.register(Category)


@admin.register(Product)
class VendorProductAdmin(admin.ModelAdmin):
    list_display = ["user", "shops", "coupon_code", "name", "price"]
