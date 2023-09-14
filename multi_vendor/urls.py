
from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("add-product/", views.vendor_add_product, name="vendorAddProduct"),
    path("vendor-orders/", views.product_order, name="vendorOrders"),
    path("withdraw/", views.withdraw_balance, name="withdrawBalance"),


]
