from django import forms
from django.forms import ModelForm
from .models import Files


class UploadFileForm(forms.Form):
	# TODO:
	# 	- change this from CharField to DropDown (or whatever)
    customer_number = forms.CharField(max_length=50, initial='116')
    file = forms.FileField()
