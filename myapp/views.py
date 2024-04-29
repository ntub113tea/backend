from django.shortcuts import render, redirect
from myapp.models import Purchase
from myapp import models
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib import auth

def test(request):
    return render(request,"123.html")

def index(request):
    return render(request,"index.html")

def login(request): #登入
    if request.user.is_authenticated:
        return HttpResponseRedirect('/index/')
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        auth.login(request, user)
        return HttpResponseRedirect('/index/')
    else:
        return render(request, 'login.html', locals())
    
def logout(request): #登出
    auth.logout(request)
    return HttpResponseRedirect('/index/')
    
def CustomizationForm(request): #客製化表單
    return render(request,"使用者表單.html")

#--------------------------------------------------------------------------進貨表單

def perchaselist(request): #進貨表單設定
    purchases = Purchase.objects.all().order_by('purchases_id')
    return render(request, "purchaselist.html", locals())

def purchasepostform(requset): #新增進貨資料
    if requset.method == "POST":
        herbs = requset.POST['herbs']
        herbsid = requset.POST['herbsid']
        value = requset.POST['value']
        datetime = requset.POST['datetime']
        unit = Purchase.objects.create(herbs_name=herbs, herbs_id=herbsid, purchases_value=value, purchases_time=datetime)
        return redirect('/perchaselist/')
    else:
        message = '請輸入資料'
    return render(requset, "purchasepostform.html",locals()) 

def delete(request,id=None): #刪除進貨資料
    if id!=None:
        if request.method == "POST":
            id=request.POST['cId']
        try:
            unit = Purchase.objects.get(purchases_id=id) #主鍵傳入的值跟網址的id比對
            unit.delete()
            return redirect('/perchaselist/')
        except:
            message = "讀取錯誤！"
    return render(request, "delete.html", locals())

def edit(request,id=None): #編輯進貨資料
    if request.method == "POST":
        unit = Purchase.objects.get(purchases_id=id)
        unit.herbs_name=request.POST['herbs']
        unit.purchases_value=request.POST['value']
        unit.purchases_time=request.POST['datetime']
        unit.save()
        message = '已修改'
        return redirect('/perchaselist/')
    return render(request,"edit.html",locals())

#----------------------------------------庫存表單

def herbstocklist(request): #庫存表單設定
    herbs = models.HerbStock.objects.all().order_by('herbs_id')
    return render(request, "herbstocklist.html", locals())

        



# Create your views here.
