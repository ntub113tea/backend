from django.shortcuts import render

def index(request):
    return render(request,"後台.html")

def index2(request):
    return render(request,"甜度冰塊.html")

def index3(request):
    return render(request,"選的飲料.html")
# Create your views here.
