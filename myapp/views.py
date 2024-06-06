from django.shortcuts import render, redirect
from myapp.models import Purchase,Sale,HerbStock,Customer,SymptomOfQuestion,DailyCounter,ShowResult
from myapp import models
from django.http import HttpResponse,JsonResponse
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth import authenticate, login, get_user_model
from django.db.models import Max
from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.forms import UserCreationForm
from datetime import datetime
from .form import PostForm,CustomerRegistrationForm,LoginForm,PurchaseForm
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.hashers import make_password #加密
from datetime import datetime, timedelta
import pytz,json
from django.views.decorators.csrf import ensure_csrf_cookie
from django.shortcuts import get_object_or_404


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

def rgst(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])
            user.save()
            return HttpResponseRedirect('/question/')
        else:
            # 如果表單無效，模板中顯示錯誤
            return render(request, 'rgst.html', {'form': form})
    else:
        form = CustomerRegistrationForm()
    return render(request, 'rgst.html', {'form': form})
    
#---------------------------------------------------------------客製化表單
def question(request):
    id_result= None
    if request.method == 'POST' and 'confirm_button' in request.POST: #新增按下按鈕才能更改資料庫中的數值
        nosleep = request.COOKIES.get('nosleep')
        semi_darkness = request.COOKIES.get('semi_darkness')
        sneezing = request.COOKIES.get('sneezing')
        itchiness = request.COOKIES.get('itchiness')
        stomach_anger = request.COOKIES.get('stomach_anger')
        menstrual_anguish = request.COOKIES.get('menstrual_anguish')
        bitter = request.COOKIES.get('bitter')
        
        # 獲取顧客編號
        customer_id = None
        if request.user.is_authenticated:
            customer_id = request.user.customer_id
            id_result = customer_id
        else:
            next_counter = DailyCounter.get_next_counter()
            customer_id = f'{next_counter:03d}'
            id_result = customer_id

        
        # 取得台北的時區
        taipei_tz = pytz.timezone('Asia/Taipei')
        # 獲取現在的台北時間
        taipei_now = datetime.now(taipei_tz)
        # 將台北時間轉換為 UTC 時間
        utc_now = taipei_now.astimezone(pytz.utc)

        # 將症狀資料存入資料庫         
        try:          
            # 如果用戶已經登入，則將 customer_id 設置為當前用戶的 customer_id
            # 如果用戶未登入，則將 customer_id 設置為 0
            symptom_customer_id = request.user.customer_id if request.user.is_authenticated else 0
            symptom = SymptomOfQuestion.objects.get(customer_id=symptom_customer_id)

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
                customer_id=symptom_customer_id,
                question_time=utc_now,
                q1=nosleep,
                q2=semi_darkness,
                q3=sneezing,
                q4=itchiness,
                q5=stomach_anger,
                q6=menstrual_anguish
            )

        # 如果有 nosleep，處理結果
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
                adjustment_factor = 5 / total_sum
                for i in range(len(result)):
                    dosage = float(result[i].split()[1][:-1]) * adjustment_factor
                    result[i] = result[i].split()[0] + f" {dosage:.2f}g"
                return result
            
            def choose_herb(symptom, choice, total_weight):
                herbs = {
                    "睏不好": "魚腥草",
                    "半暝還在嗨": ["白鶴靈芝", "蒲公英"],
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
                        
                        return f"{herb} {required_dosage:.2f}g"
                    else:
                        return "Invalid choice!"
                else:
                    return "Invalid symptom!"
            
            result = main()  # 調用 main 函式獲取處理結果列表
            print(result)
            herbs = []
            dosages = []
            for item in result:
                parts = item.split()
                herbs.append(parts[0])
                dosages.append(float(parts[1][:-1]))    
            herbs_mapping = {
                "魚腥草": 1, "白鶴靈芝": 2,"積雪草": 3, 
                "金銀花": 4,"蒲公英": 5,  "忍冬": 6, '野茄樹':7,'金錢薄荷':8,
                '紫蘇':9,"鴨舌黃": 10, "益母草": 11,'薄荷':12,
                '甜菊':13,'咸豐草':14
            }        
        # 根據按鈕值進行處理
            if bitter == "True":
                # 如果用戶點擊"可以"按钮
                herbs = [
                    "魚腥草",
                    "蒲公英",  # 修改此處為單一草藥
                    "金銀花",
                    "忍冬",
                    "積雪草",
                    "益母草"  # 修改此處為單一草藥
                ]
            elif bitter == "False":
                # 如果用戶點擊"不行"按钮
                herbs = [
                    "魚腥草",
                    "白鶴靈芝",  # 修改此處為單一草藥
                    "金銀花",
                    "忍冬",
                    "積雪草",
                    "鴨舌黃"  # 修改此處為單一草藥
                ]                  
           
            product_name = "客製化"  # 改成客製化
            order_time = utc_now  # 現在時間
            customer_id = request.user.customer_id if request.user.is_authenticated else id_result
            global show_result
            show_result = []
            for i in range(len(herbs)):
                show_result.append(herbs[i] + ":" + str(dosages[i]) + "g")
                Sale.objects.create(
                customer_id=customer_id,
                product_name=product_name,
                herbs_id=herbs_mapping.get(herbs[i]),
                herbs_name=herbs[i],
                sales_value=dosages[i],
                order_time=order_time
            )
            #show_id=request.user.customer_id if request.user.is_authenticated else "0"
            show=Customer.objects.filter(customer_id=customer_id).first()
            if (request.user.is_authenticated) :
                customer_name=show.customer_name
                show_result.insert(0,"顧客名字：" + customer_name)
                show_result.insert(0,"顧客電話：" + customer_id)
            else:
                show_result.insert(0,"顧客名字：" + "Guest")
                show_result.insert(0,"未登入顧客編號：" + customer_id)
            a=ShowResult.objects.get(show_id=0)
            a.data=show_result
            a.save()
            print(show_result)
            return redirect ('/question/')
    return render(request, "question.html")
    

#--------------------------------------------------歷史紀錄

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

@ensure_csrf_cookie
@user_passes_test(lambda user:user.is_staff,login_url='/accounts/login/')
def pos(request):
    if request.method == 'POST':
        try:
            # 解析 JSON 資料，注意要使用 request.body
            data = json.loads(request.body)
            orders = data.get('orders', [])  # 獲取 orders 陣列
            # 取得當前時間
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # 初始化顧客編號
            customer_id = None
            # 取得表單提交的顧客信息
            customer_info = data.get('customer_info')
            if customer_info and 'customer_id' in customer_info:
                customer_id = customer_info['customer_id']
                last_order_time = Sale.objects.filter(customer_id=customer_id).aggregate(last_order_time=Max('order_time'))['last_order_time']
                # 如果上一個訂單的時間與目前時間相同，則繼續使用該顧客編號
                if last_order_time and last_order_time == current_time:
                    pass
                else:
                    customer_id = None  # 置空顧客編號，以便後面重新生成
            # 循環處理訂單
            for order in orders:
                symptom = order.get('symptom')
                quantity = order.get('quantity')
                if not customer_id:
                    # 如果顧客編號為空，則產生一個新的顧客編號
                    next_counter = DailyCounter.get_next_counter()
                    customer_id = f'{next_counter:03d}'
                sale_value = 2.5 * int(quantity)
                if symptom == "星夜寧靜":
                    product = "星夜寧靜"
                    herb = '魚腥草'
                    herbs_id = 1
                elif symptom == "宵福調和":
                    product = "宵福調和"
                    herb = '白鶴靈芝'
                    herbs_id = 2
                elif symptom == "鼻福寧茶":
                    product = "鼻福寧茶"
                    herb = '金銀花'
                    herbs_id = 4
                elif symptom == "悅膚寧茶":
                    product = "悅膚寧茶"
                    herb = '忍冬'
                    herbs_id = 6
                elif symptom == "慰胃來茶":
                    product = "慰胃來茶"
                    herb = '積雪草'
                    herbs_id = 3
                else: # 月悅茶
                    product = "月悅茶" 
                    herb = '鴨舌癀'
                    herbs_id = 10
                # 創建銷售紀錄
                Sale.objects.create(customer_id=customer_id, product_name=product, herbs_id=herbs_id, herbs_name=herb, sales_value=sale_value, order_time=current_time)
                
            return JsonResponse({'message': '點餐成功！', 'refresh': True})
        except json.JSONDecodeError as e:
            return JsonResponse({'error': '無效的 JSON 資料'}, status=400)
    show=ShowResult.objects.filter(show_id=0).first()
    show_result=show.data
    print(show_result)
    return render(request, "POS介面  new.html", {'show_result': show_result})


    """ symptom = request.COOKIES.get('finalsymptom')

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
        message = '請輸入資料' """
    

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
    return redirect('/index/')

def register(request): #用戶註冊
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])
            user.save()
            return HttpResponseRedirect('/question/')
        else:
            # 如果表單無效，模板中顯示錯誤
            return render(request, 'register.html', {'form': form})
    else:
        form = CustomerRegistrationForm()
    return render(request, 'register.html', {'form': form})

#--------------------------------------------------------------------------進貨表單

def perchaselist(request): #進貨表單設定
    purchases = Purchase.objects.all().order_by('purchases_id')
    return render(request, "purchaselist.html", locals())

def purchasepostform(request): #新增進貨資料
    if request.method == "POST":
        postform = PostForm(request.POST)
        if postform.is_valid():
            herbs_id = postform.cleaned_data['herbs_name']
            supply_id = postform.cleaned_data['supply_id']
            purchases_value = postform.cleaned_data['purchases_value']
            purchases_time = postform.cleaned_data['purchases_time']
            
            # 從 choices 中獲取對應的名稱
            herbs_name = dict(PostForm.HERBS_CHOICES).get(herbs_id)
            
            if herbs_id:  # 確保herbs_id不是空的
                unit = Purchase.objects.create(
                    herbs_name=herbs_name,
                    supply_id=supply_id,
                    herbs_id=herbs_id, 
                    purchases_value=purchases_value, 
                    purchases_time=purchases_time
                )
            return redirect('/perchaselist/')
    else:
        postform = PostForm()
    return render(request, "purchasepostform.html", {'postform': postform})

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

def edit(request, id=None):  # 編輯進貨資料
    unit = get_object_or_404(Purchase, purchases_id=id)
    if request.method == "POST":
        form = PurchaseForm(request.POST)
        if form.is_valid():
            unit.herbs_id = form.cleaned_data['herbs_id']
            herbs_name_mapping = {
                '1': '魚腥草',
                '2': '白鶴靈芝',
                '3': '積雪草',
                '4': '金銀花',
                '5': '蒲公英',
                '6': '忍冬',
                '7': '野茄樹',
                '8': '金錢薄荷',
                '9': '紫蘇',
                '10': '鴨舌癀',
                '11': '益母草',
                '12': '薄荷',
                '13': '甜菊',
                '14': '咸豐草',
            }
            unit.herbs_name = herbs_name_mapping.get(unit.herbs_id, '')
            unit.supply_id = form.cleaned_data['supply_id']
            unit.purchases_value = form.cleaned_data['purchases_value']
            unit.purchases_time = form.cleaned_data['purchases_time']
            unit.save()
            return redirect('/perchaselist/')
    else:
        form = PurchaseForm(initial={
            'herbs_id': unit.herbs_id,
            'supply_id': unit.supply_id,
            'purchases_value': unit.purchases_value,
            'purchases_time': unit.purchases_time
        })
    
    return render(request, "edit.html", {'form': form, 'unit': unit})

#----------------------------------------庫存表單

def herbstocklist(request): #庫存表單設定
    herbs = models.HerbStock.objects.all().order_by('herbs_id')
    return render(request, "herbstocklist.html", locals())

def check_inventory(request):
    low_inventory_herbs = HerbStock.objects.filter(current_stock__lt=30)  #藥草存貨30以下發出警告
    low_inventory_list = [{'herbs_name': herb.herbs_name, 'current_stock': herb.current_stock} for herb in low_inventory_herbs]
    return JsonResponse({'low_inventory': low_inventory_list})

#----------------------------------------銷售表單

def salelist(request): #銷售表單設定
    sort_order = request.GET.get('saleid')
    if sort_order == 'ascending':
        sales = Sale.objects.all().order_by('sale_id')
    else:
        sales = Sale.objects.all().order_by('-sale_id')
    return render(request, "salelist.html", {'sales': sales})

def salelist_staff(request): #銷售表單(員工)設定
    sort_order = request.GET.get('saleid')
    if sort_order == 'ascending':
        sales = Sale.objects.all().order_by('sale_id')
    else:
        sales = Sale.objects.all().order_by('-sale_id')
    return render(request, "salelist_staff.html", {'sales': sales})

# Create your views here.
