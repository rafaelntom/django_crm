from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
import ipdb


# Create your views here.
def home(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request=request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in!")
            return redirect("home")
        else:
            messages.error(
                request, "There was an error logging in, please try again..."
            )
            return redirect("home")

    return render(request, "home.html")


def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out")
    return redirect("home")
