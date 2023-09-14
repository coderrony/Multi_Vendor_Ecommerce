
from django.urls import path
from .import views


urlpatterns = [

    path("checkout/", views.checkout, name="checkout"),
    path("pay/", views.payment, name="payment"),
    path("result/", views.complete_page, name="result"),
    path("purchase/<orderId>/<paymentId>/<card_type>/",
         views.purchase, name="purchase"),
    path("orders/", views.order_view, name="orders"),
]
