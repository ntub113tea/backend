from django import forms

class PostForm(forms.Form):
    herbs_id = forms.IntegerField(required=True)
    purchases_value = forms.FloatField(required=True)
    purchases_time = forms.DateTimeField(required=True)