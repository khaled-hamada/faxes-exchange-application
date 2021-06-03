from django import forms
from .models import fax

class newfaxForm(forms.Form):
    sader = forms.IntegerField()
    sader_edara = forms.IntegerField()
    url = forms.FileField()

class editfaxForm(forms.Form):
    title = forms.CharField(max_length=30)
    comments = forms.CharField(max_length=255)
    reply_dept = forms.CharField(max_length=200)