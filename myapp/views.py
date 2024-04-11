from django.shortcuts import render, redirect
from myapp.models import Purchase

def index(request):
    return render(request,"後台.html")

def index2(request):
    return render(request,"甜度冰塊.html")

def index3(request):
    return render(request,"選的飲料.html")

def perchaselist(request): #進貨表單設定
    purchases = Purchase.objects.all().order_by('purchases_id')
    return render(request, "purchaselist.html", locals())

def purchasepostform(requset): #新增進貨資料
    if requset.method == "POST":
        herbs = requset.POST['herbs']
        value = requset.POST['value']
        datetime = requset.POST['datetime']
        unit = Purchase.objects.create(herbs_name=herbs, purchases_value=value, purchases_time=datetime)
        return redirect('/perchaselist/')
    else:
        message = '請輸入資料'
    return render(requset, "purchasepostform.html",locals())


# Create your views here.
