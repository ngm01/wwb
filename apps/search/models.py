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

	def searchCatalog(self, searchList):
		data = []
		#startTime = time.strftime("%m/%d/%Y %I:%M:%S %p", time.localtime())
		# TODO:
		#	- Add something that removes any blank lines from the end of the file
		with open(searchList, 'r') as f:
			reader = csv.reader(f)
			for row in reader:
				data.append({'item_number': row[0],
					'title': row[1],
					'isbn': row[9],
					'match': ''})

		del data[0]
		for book in data:
			print "Checking", book['item_number']
			book['isbn'] = book['isbn'].replace("ISBN ", "")
			url = self.url_begin + book['isbn'] + self.url_end
			urlReq = requests.get(url)
			soup = BeautifulSoup(urlReq.text, 'html.parser')
			exec('soup_parse = self.element')
			elem_list = self.element.split(',')
			parse_element = soup.find(elem_list[0], {elem_list[1]:elem_list[2]})
			if self.keywords in parse_element.text:
				book['match'] = "No Match"
			else:
				book['match'] = "Possible Match"

		return data

class Files(models.Model):

	upload = models.FileField()


class Book(models.Model):
	pass
