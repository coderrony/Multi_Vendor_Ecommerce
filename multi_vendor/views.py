from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from app_shop.models import Product
from .forms import VendorProductForm
from app_order.models import Order
from datetime import datetime
import plotly.express as px
# Create your views here.


@login_required(login_url="login")
def dashboard(request):

    earningAmount = 0  # show on th main ui
    total_order = 0
    earningPerOrder = 0
    dateSave = []
    earningSave = []
    isFound = False
    for order in Order.objects.all():

        for item in order.orderItems.all():
            if (item.item.user == request.user):
                isFound = True
                total_order += 1
                earningAmount += item.item.price
                earningPerOrder += item.item.price
        if isFound:
            date_string = str(order.created).split(" ")[0]
            date_format = "%Y-%m-%d"
            # Convert the string to a date
            date_object = datetime.strptime(date_string, date_format)
            dateSave.append(date_object)
            earningSave.append(earningPerOrder)
            isFound = False
            earningPerOrder = 0

    # data insert in line chart vertical and horizontal
    fig = px.line(
        x=[d for d in dateSave],
        y=[v for v in earningSave],
        title="Earning Visualization ",
        labels={"x": "Date", 'y': "Earning"}
    )

    fig.update_layout(title={
        'font_size': 22,
        'xanchor': 'center',
        'x': 0.5
    })

    chart = fig.to_html()

    return render(request, "homeDash.html", context={"earning": int((earningAmount/100) * 10), "total_order": total_order, "chart": chart})


# @login_required(login_url="login")
def vendor_add_product(request):
    products = Product.objects.filter(user=request.user)
    form = VendorProductForm()
    if request.method == "POST":
        form = VendorProductForm(request.POST,  request.FILES)
        if form.is_valid():
            vendor_form = form.save(commit=False)
            vendor_form.user = request.user
            vendor_form.save()
            return redirect("vendorAddProduct")

    return render(request, "vendorProduct.html", context={"products": products, "form": form})


@login_required(login_url="login")
def product_order(request):

    ordered = []
    for order in Order.objects.all():
        for item in order.orderItems.all():
            if (item.item.user == request.user):
                # print(item.item)
                ordered.append(
                    {"name": item.item.name, "quantity": item.quantity})
                print(item.quantity)
                print(item.item.name)
    print(ordered[0])
    return render(request, "vendorOrder.html", context={"ordered": ordered})


@login_required(login_url="login")
def withdraw_balance(request):
    earningAmount = 0
    for order in Order.objects.all():
        for item in order.orderItems.all():
            if (item.item.user == request.user):
                earningAmount += item.item.price

    return render(request, "withdraw.html", context={"earning": int((earningAmount/100) * 10)})
