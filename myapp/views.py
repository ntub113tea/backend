from django.shortcuts import render, redirect
from myapp.models import Purchase,Sale,HerbStock
from myapp import models
from django.http import HttpResponse,JsonResponse
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from datetime import datetime
from .form import PostForm,CustomerRegistrationForm,LoginForm
from django.contrib.auth.hashers import make_password #加密
def test(request):
    return render(request,"123.html")
def administrator(request):
    return render(request,"administrator.html")
def index(request):
    return render(request,"index.html")

#--------------------------------------------pos系統(非客製化)

def pos(request):

    symptom = request.COOKIES.get('finalsymptom')

    if symptom:
        customer = 0
        sale_value = 2.5
        time = datetime.now().strftime("%Y-%m-%d %H:%M")
        if symptom == "星夜寧靜":
            product = "星夜寧靜"
            herb = HerbStock.objects.get(herbs=1)
        elif symptom == "宵福調和":
            product = "宵福調和"
            herb = HerbStock.objects.get(herbs=2)
        elif symptom == "鼻福寧茶":
            product = "鼻福寧茶"
            herb = HerbStock.objects.get(herbs=4)
        elif symptom == "悅膚寧茶":
            product = "悅膚寧茶"
            herb = HerbStock.objects.get(herbs=6)
        elif symptom == "慰胃來茶":
            product = "慰胃來茶"
            herb = HerbStock.objects.get(herbs=3)
        else: #月悅茶
            product = "月悅茶" 
            herb = HerbStock.objects.get(herbs=10)
        
        Sale.objects.create(customer_id=customer,product_name=product,herbs=herb,sales_value=sale_value,order_time=time)
        return redirect('//')
    else:
        message = '請輸入資料'
    return render(request,"POS介面.html",locals())

#----------------------------------------------------登入登出註冊
def login_view(request): #用戶登入
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/index/') 
            else:
                return render(request, 'login.html', {'form': form, 'error': '帳號或密碼輸入錯誤'})
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})   
def logout(request): #用戶登出
    auth.logout(request)
    return HttpResponseRedirect('/index/')

def register(request): #用戶註冊
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])
            user.save()
            return HttpResponseRedirect('/index/')
        else:
            # 如果表單無效，模板中顯示錯誤
            return render(request, 'register.html', {'form': form})
    else:
        form = CustomerRegistrationForm()
    return render(request, 'register.html', {'form': form})
    
def CustomizationForm(request): #客製化表單
    return render(request,"使用者表單.html")

#--------------------------------------------------------------------------進貨表單

def perchaselist(request): #進貨表單設定
    purchases = Purchase.objects.all().order_by('purchases_id')
    return render(request, "purchaselist.html", locals())

def purchasepostform(request): #新增進貨資料
    if request.method == "POST":
        postform=PostForm(request.POST)
        if postform.is_valid():
            herbs_id = postform.cleaned_data['herbs_name']
            herbs_name = dict(PostForm.HERBS_CHOICES).get(herbs_id, "Unknown Herb")
            purchases_value = postform.cleaned_data['purchases_value']
            purchases_time =postform.cleaned_data['purchases_time']
            if herbs_id:  # 确保herbs_id非空
                unit = Purchase.objects.create(herbs_name=herbs_name, herbs_id=herbs_id, purchases_value=purchases_value, purchases_time=purchases_time)
            return redirect('/perchaselist/')
        else:
            message = postform.errors.get('herbs_name', ['請檢查輸入的數據'])[0]  # 藥草名稱錯誤訊息
    else:
        message = '請輸入進貨資料'
        postform=PostForm()
    return render(request, "purchasepostform.html", {'postform': postform, 'message': message})

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

def check_inventory(request):
    low_inventory_herbs = HerbStock.objects.filter(current_stock__lt=30)  #藥草存貨30以下發出警告
    low_inventory_list = [{'herbs_name': herb.herbs_name, 'current_stock': herb.current_stock} for herb in low_inventory_herbs]
    return JsonResponse({'low_inventory': low_inventory_list})
#----------------------------------------銷售表單

def salelist(request): #庫存表單設定
    sales = Sale.objects.all().order_by('sale_id')
    return render(request, "salelist.html", locals())

        



# Create your views here.
