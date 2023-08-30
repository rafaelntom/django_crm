from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record


# Create your views here.
def home(request):
    records = Record.objects.all()

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

    return render(request, "home.html", {"records": records})


def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out")
    return redirect("home")


def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]

            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You have been successfully registered!")
            return redirect("home")
    else:
        form = SignUpForm()

    return render(request, "register.html", {"form": form})


def customer_record(request, pk):
    if request.user.is_authenticated:
        customer = Record.objects.get(pk=pk)
        return render(request, "record.html", {"customer": customer})
    else:
        messages.error(request, "You must be authenticated to access this page.")
        return redirect("home")


def customer_delete(request, pk):
    if request.user.is_authenticated:
        customer = Record.objects.get(pk=pk)
        customer.delete()
        messages.success(request, "Record was successfully deleted!")
        return redirect("home")
    else:
        messages.error(request, "You must be authenticated to access this page.")
        return redirect("home")


def create_record(request):
    if request.user.is_authenticated:
        form = AddRecordForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(request, "Record was successfully created!")
                return redirect("home")

        return render(request, "create_record.html", {"form": form})
    else:
        messages.error(request, "You must be authenticated to access this page.")
        return redirect("home")


def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request, "Record was successfully updated!")
            return redirect("home")
        return render(request, "update_record.html", {"form": form})
    else:
        messages.success(request, "You must be authenticated to access this page..")
        return redirect("home")
