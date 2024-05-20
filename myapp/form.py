from django import forms
from .models import Customer
from django.core.exceptions import ValidationError
import re

class PostForm(forms.Form):   #進貨資料驗證
    HERBS_CHOICES = [
         ('', '--- 請選擇藥草 ---'),
        ('1', '魚腥草'), ('2', '白鶴靈芝'), ('3', '積雪草'), 
        ('4', '金銀花'), ('5', '蒲公英'), ('6', '忍冬'), 
        ('7', '野茄樹'), ('8', '金錢薄荷'), ('9', '紫蘇'), 
        ('10', '鴨舌癀'), ('11', '益母草'), ('12', '薄荷'), 
        ('13', '甜菊'), ('14', '咸豐草'),
    ]
    herbs_name = forms.ChoiceField(
        required=False,
        choices=HERBS_CHOICES,
        label='Herbs')
    herbs_id = forms.IntegerField(required=True,min_value=1)
    supply_id=forms.CharField(label='供應商編號', max_length=45)
    purchases_value = forms.FloatField(required=True)
    purchases_time = forms.DateTimeField(required=True, widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    def clean_herbs_name(self):
        herbs_name = self.cleaned_data['herbs_name']
        if herbs_name == '':
            raise ValidationError("請選擇一種藥草")
        return herbs_name

class CustomerRegistrationForm(forms.ModelForm):  #註冊（處理用戶輸入）
    password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'id': 'password' }),label='生日') 
    #autocomplete': 'new-password告訴瀏覽器這是新的密碼 不應該保存任何值
    password_confirmation = forms.CharField(widget=forms.PasswordInput(), label='確認生日')
    sex = forms.ChoiceField(
        choices=Customer.GENDER_CHOICES,
        widget=forms.RadioSelect,
        label='性別'  
    )
    customer_id = forms.CharField(label='電話號碼', max_length=10,)
    class Meta:
        model = Customer
        fields = ['customer_id', 'password', 'customer_name', 'sex','line_id',]
        labels = {
            'customer_name': '姓名',
            'line_id': 'LINE ID（可選填）'
        }
    def clean_customer_id(self):
        customer_id = self.cleaned_data['customer_id']
        if not customer_id.startswith('09'):
            raise forms.ValidationError("電話號碼必須為09開頭")
        if Customer.objects.filter(customer_id=customer_id).exists():
            raise ValidationError("此電話號碼已被註冊")
        return customer_id

    def clean_customer_name(self):
        customer_name = self.cleaned_data.get('customer_name')
        if re.search(r'\d', customer_name):  # 使用正規表達檢查是否有數字
            raise ValidationError("姓名不應包含數字")
        return customer_name
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not re.match(r'^\d{7}$', password):  # 確保密碼為7位數字
            raise ValidationError("生日必須是7位數字")
        month = int(password[3:5])
        day = int(password[5:7])

        if not (1 <= month <= 12):
            raise ValidationError("月份必須在1到12之間")
        if not (1 <= day <= 31):
            raise ValidationError("日期必須在1到31之間")

        return password
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirmation = cleaned_data.get("password_confirmation")

        if password and password_confirmation:
            if password != password_confirmation:
                self.add_error('password_confirmation', "密碼不一致")
            else:
                cleaned_data['birthday'] = password_confirmation  # 将 password_confirmation 存入 birthday
    
        return cleaned_data
    def save(self, commit=True):
        customer = super().save(commit=False)
        customer.birthday = self.cleaned_data.get('birthday')  # 显式地将 birthday 字段保存到模型中
        if commit:
            customer.save()
        return customer
    
class LoginForm(forms.Form): #登入系統
    username = forms.CharField(label='電話號碼', max_length=10,)
    password = forms.CharField(label='　　生日', widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}))