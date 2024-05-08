from django import forms
from .models import Customer
from django.core.exceptions import ValidationError
import re

class PostForm(forms.Form):   #進貨資料驗證
    HERBS_CHOICES = [
        ('魚腥草', '魚腥草'),
        ('白鶴靈芝', '白鶴靈芝'),
        ('積雪草', '積雪草'),
        ('金銀花', '金銀花'),
        ('蒲公英', '蒲公英'),
        ('忍冬', '忍冬'),
        ('野茄樹', '野茄樹'),
        ('金錢薄荷', '金錢薄荷'),
        ('紫蘇', '紫蘇'),
        ('鴨舌癀', '鴨舌癀'),
        ('益母草', '益母草'),
        ('薄荷', '薄荷'),
        ('甜菊', '甜菊'),
        ('咸豐草', '咸豐草'),
    ]
    herbs_name = forms.ChoiceField(
        required=True,
        choices=HERBS_CHOICES,
        label='Herbs')
    herbs_id = forms.IntegerField(required=True,min_value=1,max_value=14)
    purchases_value = forms.FloatField(required=True,min_value=0)
    purchases_time = forms.DateTimeField(required=True, widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))

class CustomerRegistrationForm(forms.ModelForm):  #註冊（處理用戶輸入）
    password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'id': 'password' }),label='密碼') 
    #autocomplete': 'new-password告訴瀏覽器這是新的密碼 不應該保存任何值
    password_confirmation = forms.CharField(widget=forms.PasswordInput(), label='確認密碼')
    sex = forms.ChoiceField(
        choices=Customer.GENDER_CHOICES,
        widget=forms.RadioSelect,
        label='性別'
        
    )
    class Meta:
        model = Customer
        fields = ['customer_id', 'password', 'customer_name', 'sex', 'age','line_id']
        labels = {
            'customer_id': '電話號碼',
            'customer_name': '姓名',
            'age': '年齡',
            'line_id': 'LINE ID（可選填）'
        }
    def clean_customer_id(self):
        customer_id = self.cleaned_data['customer_id']
        if Customer.objects.filter(customer_id=customer_id).exists():
            raise ValidationError("此電話號碼已被註冊。")
        return customer_id

    def clean_customer_name(self):
        customer_name = self.cleaned_data.get('customer_name')
        if re.search(r'\d', customer_name):  # 使用正規表達檢查是否有數字
            raise ValidationError("姓名不應包含數字")
        return customer_name
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirmation = cleaned_data.get("password_confirmation")

        if password and password_confirmation and password != password_confirmation:
            self.add_error('password_confirmation', "密碼不一致")

        return cleaned_data
class LoginForm(forms.Form): #登入系統
    username = forms.CharField(label='電話號碼', max_length=100,)
    password = forms.CharField(label='密碼', widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}))