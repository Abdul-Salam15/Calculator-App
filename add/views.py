from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, "index.html")

def solve(request):
    value1 = int(request.POST['num1'])
    value2 = int(request.POST['num2'])
    op = request.POST['op']
    if op == "+":
        res = value1 + value2
    elif op == "-":
        res = value1 - value2
    elif op == "*":
        res = value1 * value2
    elif op == "/":
        res = value1 / value2

    return render(request, "result.html", {
        "result" : res
    })