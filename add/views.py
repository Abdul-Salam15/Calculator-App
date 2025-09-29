from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Calculation
from django.utils import timezone
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required(login_url="login")
def index(request):
    return render(request, "index.html")

#Register
def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Registration successful!")
            return redirect("login")
        else:
            # 🚨 DO NOT redirect here — re-render the form with errors
            return render(request, "register.html", {"form": form})
    else:
        form = CustomUserCreationForm()
    return render(request, "register.html", {"form": form})

#Login
def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Logged in successfully!")
            return redirect("home")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})

# Logout
def user_logout(request):
    logout(request)
    return redirect("login")


@login_required
def solve(request):
    value1 = int(request.POST['num1'])
    value2 = int(request.POST['num2'])
    op = request.POST['op']

    # Perform calculation
    if op == "+":
        res = value1 + value2
    elif op == "-":
        res = value1 - value2
    elif op == "*":
        res = value1 * value2
    elif op == "/":
        res = value1 / value2 if value2 != 0 else "Error: Division by zero"
    elif op == "^":
        res = value1 ** value2
    elif op == "%":
    res = str((value1 / 100) * value2) + '%'
    else:
        res = "Invalid operator"

    # Build expression string
    expression = f"{value1} {op} {value2}"

    # Save in DB (with or without user)
    if request.user.is_authenticated:
        Calculation.objects.create(
            user=request.user,
            expression=expression,
            result=str(res)
        )
    else:
        Calculation.objects.create(
            expression=expression,
            result=str(res)
        )

    # Retrieve old history or empty list (from session)
    history = request.session.get("history", [])

    # Add new calculation at the start
    history.insert(0, {
        "expression": expression,
        "result": res,
        "timestamp": timezone.now().strftime("%Y-%m-%d %H:%M:%S"),
    })

    # Save back to session
    request.session["history"] = history

    return render(request, "result.html", {"result": res})

from django.contrib.auth.decorators import login_required

@login_required   # ensures only logged-in users can access
def history(request):
    history = Calculation.objects.filter(user=request.user).order_by("-timestamp")
    return render(request, "history.html", {"history": history})
