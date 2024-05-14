from django.shortcuts import render, redirect
from myapp.models import Purchase,Sale,HerbStock,Customer,SymptomOfQuestion
from myapp import models
from django.http import HttpResponse,JsonResponse
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth import authenticate, login, get_user_model

from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.forms import UserCreationForm
from datetime import datetime
from .form import PostForm,CustomerRegistrationForm,LoginForm
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.hashers import make_password #加密
from datetime import datetime, timedelta
import pytz

@user_passes_test(lambda user:user.is_superuser,login_url='/accounts/login/')
def manage(request):
    return render(request,"manage.html")

@user_passes_test(lambda user:user.is_staff,login_url='/accounts/login/')
def staff(request):
    return render(request,"staff.html")

def url(request):
    return render(request,"url.html")

def index(request):
    return render(request,"index.html")

def manage_users(request):
    user_form = UserCreationForm(request.POST or None)
    Customer = get_user_model()
    users = Customer.objects.all()
    
    if request.method == 'POST':
        if user_form.is_valid():
            user_form.save()
            return redirect('manage_users')

    return render(request, 'manage_users.html', {'user_form': user_form, 'users': users})

def manage_groups(request):
    if request.method == 'POST':
        # 处理表单提交，创建/编辑用户组
        # 分配权限等操作
        pass
    else:
        groups = Group.objects.all()
        permissions = Permission.objects.all()
        context = {'groups': groups, 'permissions': permissions}
        return render(request, 'manage_groups.html', context)
    
#---------------------------------------------------------------

def question(request): #客製化問卷
    nosleep = request.COOKIES.get('nosleep')
    semi_darkness=request.COOKIES.get('semi_darkness')
    sneezing=request.COOKIES.get('sneezing')
    itchiness=request.COOKIES.get('itchiness')
    stomach_anger=request.COOKIES.get('stomach_anger')
    menstrual_anguish=request.COOKIES.get('menstrual_anguish')
    customer_id = request.user.customer_id if request.user.is_authenticated else 0

# 取得台北的時區
    taipei_tz = pytz.timezone('Asia/Taipei')

# 獲取現在的台北時間
    taipei_now = datetime.now(taipei_tz)

# 將台北時間轉換為 UTC 時間
    utc_now = taipei_now.astimezone(pytz.utc)

    # 將症狀資料存入資料庫
    try:
        symptom = SymptomOfQuestion.objects.get(customer_id=customer_id)
        
        # 如果找到現有的記錄，則更新問題資料
        symptom.question_time = utc_now
        symptom.q1 = nosleep
        symptom.q2 = semi_darkness
        symptom.q3 = sneezing
        symptom.q4 = itchiness
        symptom.q5 = stomach_anger
        symptom.q6 = menstrual_anguish
        symptom.save()
    except SymptomOfQuestion.DoesNotExist:
        # 如果不存在，則創建一個新的記錄
        SymptomOfQuestion.objects.create(
            customer_id=customer_id,
            question_time=utc_now,
            q1=nosleep,
            q2=semi_darkness,
            q3=sneezing,
            q4=itchiness,
            q5=stomach_anger,
            q6=menstrual_anguish
        )
    if nosleep:
        def main():
            symptoms = [
                "睏不好",
                "半暝還在嗨",
                "早上哈啾",
                "癢癢",
                "胃生氣",
                "厭世生理期"
            ]
            value = [
                nosleep,
                semi_darkness,
                sneezing,
                itchiness,
                stomach_anger,
                menstrual_anguish
            ]

            result = []
            total_weight = 5  # 定義藥材克數的總和
            for i in range(6):
                choice = value[i]
                result.append(choose_herb(symptoms[i], choice, total_weight))

            # 如果六種藥材的克數加總超過5，則進行額外調整
            total_sum = sum(float(item.split()[1][:-1]) for item in result)
            if total_sum > 5:
                adjustment_factor = 5 / total_sum
                for i in range(len(result)):
                    dosage = float(result[i].split()[1][:-1]) * adjustment_factor
                    result[i] = result[i].split()[0] + f" {dosage:.2f}g"
            return result
        def choose_herb(symptom, choice, total_weight):
            herbs = {
                "睏不好": "魚腥草",
                "半暝還在嗨": ["白鶴靈芝(不苦)", "蒲公英(苦)"],
                "早上哈啾": "金銀花",
                "癢癢": "忍冬",
                "胃生氣": "積雪草",
                "厭世生理期": ["鴨舌黃", "益母草"]
            }

            dosage = {
                "1": 0.5,
                "2": 1.0,
                "3": 1.5,
                "4": 2.0,
                "5": 2.5
            }

            if symptom in herbs:
                herb = herbs[symptom]
                if isinstance(herb, list):
                    herb = "or".join(herb)
                if choice in dosage:
                    # 計算每個症狀所需的藥材克數
                    required_dosage = dosage[choice]
                    # 計算調整比例，以確保所有藥材的總和為 total_weight
                    adjustment_factor = total_weight / sum(dosage.values())
                    # 調整每個症狀所需的藥材克數
                    adjusted_dosage = required_dosage * adjustment_factor
                    # 限制小數位數最多為兩位
                    adjusted_dosage = round(adjusted_dosage, 2)
                    return f"{herb} {adjusted_dosage:.2f}g"
                else:
                    return "Invalid choice!"
            else:
                return "Invalid symptom!"
        result = main()  # 調用 main 函式獲取處理結果列表
        return render(request, "question.html", {'result': result})
    return render(request,"question.html")

def history_view(request):
    # 確保只有登入的用戶才能訪問歷史記錄頁面
    if not request.user.is_authenticated:
        return render(request, 'login_required.html')

    # 獲取當前用戶的電話號碼
    customer_id = request.user.customer_id

    # 獲取當前用戶的所有歷史記錄
    history_records = SymptomOfQuestion.objects.filter(customer_id=customer_id)

    return render(request, 'history.html', {'history_records': history_records})
#--------------------------------------------pos系統(非客製化)

@user_passes_test(lambda user:user.is_staff,login_url='/accounts/login/')
def pos(request):

    symptom = request.COOKIES.get('finalsymptom')

    if symptom:
        customer = 0
        sale_value = 2.5
        time = datetime.now().strftime("%Y-%m-%d %H:%M")
        if symptom == "星夜寧靜":
            product = "星夜寧靜"
            herb = 1
        elif symptom == "宵福調和":
            product = "宵福調和"
            herb = 2
        elif symptom == "鼻福寧茶":
            product = "鼻福寧茶"
            herb = 4
        elif symptom == "悅膚寧茶":
            product = "悅膚寧茶"
            herb = 6
        elif symptom == "慰胃來茶":
            product = "慰胃來茶"
            herb = 3
        else: #月悅茶
            product = "月悅茶" 
            herb = 10
        
        Sale.objects.create(customer_id=customer,product_name=product,herbs_id=herb,sales_value=sale_value,order_time=time)
        return redirect('/manage/')
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
            if user is not None and user.is_active:
                if user.is_superuser:
                    # 如果用戶是管理員,跳轉到管理員首頁
                    login(request, user)
                    return redirect('/manage/')
                if user.is_staff:
                    # 如果用戶是員工,跳轉到員工首頁
                    login(request, user)
                    return redirect('/staff/')
                else:
                    login(request, user)
                    return redirect('/question/')
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
