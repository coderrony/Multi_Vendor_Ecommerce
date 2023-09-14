from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Cart, Order
from app_shop.models import Product
# from Multi_Vendor.models import VendorProduct
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


@login_required(login_url="login")
def add_to_cart(request, pk):

    item = get_object_or_404(Product, pk=pk)

    # get_or_create method get this product are already have if not then create a cart from that information
    # and return a tuple
    order_item = Cart.objects.get_or_create(
        item=item, user=request.user, purchased=False)
    print("order_item -> ", order_item)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    # print("order_qs -> ", order_qs)

    if order_qs.exists():
        order = order_qs[0]
        if order.orderItems.filter(item=item).exists():
            order_item[0].quantity += 1
            order_item[0].save()
            messages.info(request, "This item quantity was updated.")
            return redirect("home")
        else:
            order.orderItems.add(order_item[0])
            messages.info(request, "This Item was added to your cart.")
            return redirect("home")
    else:
        order = Order(user=request.user)
        order.save()
        order.orderItems.add(order_item[0])
        messages.info(request, "This item was added to your cart")
        return redirect("home")


@login_required(login_url="login")
def cart_view(request):
    carts = Cart.objects.filter(user=request.user, purchased=False)
    orders = Order.objects.filter(user=request.user, ordered=False)
    # print(order.orderItems)
    # print(order.paymentId)
    if carts.exists() and orders.exists():
        order = orders[0]

        return render(request, "cart.html", context={"carts": carts, "order": order})
    else:
        messages.warning(request, "you don't have any item in your cart")
        return redirect("home")


@login_required(login_url="login")
def remove_from_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.orderItems.filter(item=item).exists():
            order_item = Cart.objects.filter(
                item=item, user=request.user, purchased=False)[0]
            order.orderItems.remove(order_item)
            order_item.delete()
            messages.warning(request, "This item was removed from your cart")
            return redirect("cart")
        else:
            messages.info(request, "This item was not in you cart")
            return redirect("home")

    else:
        messages.info(request, "You don't have an active order")
        return redirect("home")


@login_required(login_url="login")
def increase_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.orderItems.filter(item=item).exists():
            order_item = Cart.objects.filter(
                item=item, user=request.user, purchased=False)[0]
            if order_item.quantity >= 1:
                order_item.quantity += 1
                order_item.save()
                messages.info(
                    request, f"{item.name} quantity has been updated ")
                return redirect("cart")
        else:
            messages.info(request, f"{item.name} is not in your cart ")
            return redirect("home")

    else:
        messages.info(request, "You don't have active order")
        return redirect("home")


@login_required(login_url="login")
def decrease_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.orderItems.filter(item=item).exists():
            order_item = Cart.objects.filter(
                item=item, user=request.user, purchased=False)[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
                messages.info(
                    request, f"{item.name} quantity has been updated ")
                return redirect("cart")
            else:
                order.orderItems.remove(order_item)
                order_item.delete()
                messages.warning(
                    request, f" {item.name} This item was removed from your cart")
                return redirect("cart")
        else:
            messages.info(request, f"{item.name} is not in your cart ")
            return redirect("cart")

    else:
        messages.info(request, "You don't have active order")
        return redirect("home")
