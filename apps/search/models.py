from __future__ import unicode_literals

from django.db import models

from ..login.models import User
import openpyxl
import csv, requests, time
from bs4 import BeautifulSoup

class Customer(models.Model):

	cust_number = models.IntegerField()
	account_suffix = models.CharField(max_length=5, default='z')
	cust_name = models.CharField(max_length=255)
	url_begin = models.TextField()
	url_end = models.TextField()
	catalog_type = models.CharField(max_length=25, default='B')
	element = models.CharField(max_length=255)
	keywords = models.CharField(max_length=255)

class Files(models.Model):

	upload = models.FileField()


class Book(models.Model):
	pass
