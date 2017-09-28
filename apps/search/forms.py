from django import forms
from django.forms import ModelForm
from .models import Files


class UploadFileForm(forms.Form):
	# TODO:
	# 	- this needs to be a multiple value field...
	#	...which is called what, in Django-lingo?
	# 	- it needs to draw from the list of customer objects in the database...
	CUSTOMER_CHOICES = (('116', '116 - Princeton'),('544', '544 - University of British Columbia'))
	customer_number = forms.ChoiceField(choices=CUSTOMER_CHOICES)
	file = forms.FileField()