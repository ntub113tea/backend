from django import forms

class PostForm(forms.Form):
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
