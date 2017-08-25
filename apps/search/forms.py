from django import forms
from django.forms import ModelForm
from .models import Files


class UploadFileForm(forms.Form):
    customer = forms.CharField(max_length=50, initial='116')
    file = forms.FileField()
