from django.shortcuts import render, redirect
from .models import BillingAddress
from app_order.models import Cart
from .forms import BillingForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from app_order.models import Order
from django.urls import reverse
from sslcommerz_lib import SSLCOMMERZ

from django.views.decorators.csrf import csrf_exempt
import uuid
# Create your views here.


@login_required(login_url="login")
def checkout(request):
    is_fully_filled = False
    saved_address = BillingAddress.objects.get_or_create(
        user=request.user)  # return tuple

    form = BillingForm(instance=saved_address[0])
    if request.method == "POST":
        form = BillingForm(request.POST, instance=saved_address[0])
        if form.is_valid():
            form.save()
            messages.info(request, f"Shipping Address Saved")

    order_qs = Order.objects.filter(user=request.user, ordered=False)
    order_items = order_qs[0].orderItems.all()
    order_total = order_qs[0].get_totals()

    if saved_address[0].address is not None and saved_address[0].zipcode is not None and saved_address[0].city is not None and saved_address[0].country:
        is_fully_filled = True

    # print(saved_address[0].is_fully_filled)

    return render(request, "checkout.html", context={"form": form, "order_items": order_items, "order_total": order_total, "saved_address": saved_address, "is_fully_filled": is_fully_filled})


@login_required(login_url="login")
def payment(request):
    is_fully_filled = False
    saved_address = BillingAddress.objects.get_or_create(
        user=request.user)
    if saved_address[0].address is not None and saved_address[0].zipcode is not None and saved_address[0].city is not None and saved_address[0].country:
        is_fully_filled = True

    if is_fully_filled is False:
        messages.info(request, "Please Complete Shipping Address")
        return redirect("checkout")

   # status_url call when success_url call
    status_url = request.build_absolute_uri(
        reverse('result'))
    print("status_url=>", status_url)

    order_qs = Order.objects.filter(user=request.user, ordered=False)
    order_items = order_qs[0].orderItems.all()
    order_total = order_qs[0].get_totals()

    settings = {'store_id': 'abc64ea12fad7fc9',
                'store_pass': 'abc64ea12fad7fc9@ssl', 'issandbox': True}
    sslcommez = SSLCOMMERZ(settings)
    post_body = {}
    post_body['total_amount'] = order_total
    post_body['currency'] = "BDT"
    post_body['tran_id'] = str(uuid.uuid4())
    post_body['success_url'] = status_url
    post_body['fail_url'] = status_url
    post_body['cancel_url'] = status_url
    post_body['emi_option'] = request.user.email
    post_body['cus_name'] = request.user.profile.full_name
    post_body['cus_email'] = request.user.profile
    post_body['cus_phone'] = request.user.profile.phone
    post_body['cus_add1'] = request.user.profile.address_1
    post_body['cus_city'] = request.user.profile.city
    post_body['cus_country'] = request.user.profile.country
    post_body['shipping_method'] = "NO"
    post_body['multi_card_name'] = ""
    post_body['num_of_item'] = 1
    post_body['product_name'] = "Test"
    post_body['product_category'] = "Test Category"
    post_body['product_profile'] = "general"

    response = sslcommez.createSession(post_body)
    # print(response["GatewayPageURL"])

    return redirect(response["GatewayPageURL"])


@csrf_exempt
# this view get response from payment view when complete the process
def complete_page(request):
    if request.method == "POST" or request.method == "post":
        payment_date = request.POST  # request.POST has all information about payment details
        # print(request.POST)
        status = payment_date["status"]

        if status == "VALID":
            orderId = payment_date["tran_id"]
            paymentId = payment_date["val_id"]
            card_type = payment_date["card_type"].split("-")[0]

            messages.success(
                request, f" your payment completed successfully! page will be redirected ")
            return redirect("purchase", orderId, paymentId, card_type)

        elif status == "FAILED":
            messages.warning(
                request, f" your payment Failed please try again! page will be redirected ")
            return redirect("home")
    return render(request, "complete.html", context={})


@login_required(login_url="login")
def purchase(request, orderId, paymentId, card_type):
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():  # Check if there are any orders that meet the filter criteria.
        order = order_qs[0]
        order.ordered = True
        order.orderId = orderId
        order.paymentId = paymentId
        order.card_type = card_type
        order.save()

        cart_items = Cart.objects.filter(user=request.user, purchased=False)
        for item in cart_items:
            item.purchased = True
            item.save()
        return render(request, "complete.html", context={"order": order})
    else:
        order = Order.objects.filter(user=request.user, ordered=True)[0]
        print("order item => ", order.orderItems.all)

        return render(request, "complete.html", context={"order": order})


@login_required(login_url="login")
def order_view(request):
    try:
        orders = Order.objects.filter(user=request.user, ordered=True)
        context = {"orders": orders}
    except:
        messages.warning(request, "You do not have an active order")
        return redirect("home")
    return render(request, "order.html", context)
