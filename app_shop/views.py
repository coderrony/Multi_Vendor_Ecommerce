from django.shortcuts import render, redirect
from .models import Category, Product


# import views
from django.views.generic import ListView, DetailView

# mixin
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


def home(request):
    try:
        if request.user.profile.user_type == "vendor":
            return redirect("dashboard")
    except:
        pass

    products = Product.objects.all()

    return render(request, "home.html", context={"products": products})


class ProductDetails(DetailView):
    model = Product
    template_name = "product_details.html"
