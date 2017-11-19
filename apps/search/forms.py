from django import forms
from django.forms import ModelForm
from .models import Files


class UploadFileForm(forms.Form):
	# TODO:
	# Need to review python classes. I've forgotten a lot.
	# My class UploadFileForm is inheriting from the class Form in the forms module
	# so why am I importing ModelForm from django.forms?
	CUSTOMER_CHOICES = (('116', '116 - Princeton'),('544', '544 - University of British Columbia'))
	customer_number = forms.ChoiceField(choices=CUSTOMER_CHOICES)
	file = forms.FileField()