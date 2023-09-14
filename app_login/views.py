from django.shortcuts import render, redirect
# authentication
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate

# forms and model
from .models import Profile
from .forms import ProfileForm, SignUpForm
from django.http import HttpResponse

# Messages
from django.contrib import messages
# Create your views here.


def sign_up(request):
    if request.user.is_authenticated:
        return redirect("home")
    form = SignUpForm()

    if request.method == "POST":
        user_type = request.POST.get("user_type")
        form = SignUpForm(request.POST)
        if form.is_valid():
            user_form = form.save()
            profile = Profile.objects.get(user=user_form)
            profile.user_type = user_type
            profile.save()
            messages.success(request, "Account Created Successfully")
            return redirect("login")

    return render(request, "sign_up.html", context={"form": form})


def login_user(request):
    if request.user.is_authenticated:
        return redirect("home")
    form = AuthenticationForm()
    if request.method == "POST":

        # don't forget to set data variable when use AuthenticationForm
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get(
                "username")  # in User model we set USERNAME_FIELD = 'email' that't why use username as email
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)

            profile = Profile.objects.get(user=user)
            if profile.user_type == "customer":
                return redirect("home")
            else:
                return redirect("dashboard")
    return render(request, "login.html", context={"form": form})


@login_required(login_url="login")
def logout_user(request):
    logout(request)
    messages.warning(request, "You are logged out!!")
    return redirect("home")


@login_required(login_url="login")
def user_profile(request):
    profile = Profile.objects.get(user=request.user)
    form = ProfileForm(instance=profile)

    if request.method == "POST":

        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Change Saved")
    return render(request, "change_profile.html", context={"form": form})
