from django.shortcuts import render
from myapp.models import Purchase

def index(request):
    return render(request,"後台.html")

def index2(request):
    return render(request,"甜度冰塊.html")

def index3(request):
    return render(request,"選的飲料.html")

def perchaselist(request):
    purchases = Purchase.objects.all().order_by('purchases_id')
    return render(request, "purchaselist.html", locals())

# Create your views here.
