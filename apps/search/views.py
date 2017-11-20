from django.shortcuts import render, redirect, HttpResponse
from wwb.settings import MEDIA_ROOT, MEDIA_URL
from django.conf import settings
from models import Files, Customer, User
from .forms import UploadFileForm
from logics import exportToExcel, searchCatalog
import csv, magic


def index(req):
	form = UploadFileForm()
	# Checks whether there is a customer number saved in session -
	# this functions as a check whether a search has been executed or not.
	if 'customer_number' not in req.session:
		context = {'form': form,
					'media_root': MEDIA_ROOT}

		return render(req, 'search/index.html', context)
	
	else:
		customer = Customer.objects.get(cust_number=req.session['customer_number'])
		
		data = []
		req.session['count'] = 0;

		# problems begin here without file type validation of user input...
		# upload is written to 'wwbsearch.csv' in the 'uploads' directory
		# this happens in the upload() function below.
		# That is where we need to do validation.
		with open('uploads/wwbsearch.csv', 'r') as f:
			reader = csv.reader(f)
			for row in reader:
				if row[0] != '':
					data.append({'item_number': row[0],
						'title': row[1],
						'isbn': row[9],
						'match': ''})

		del data[0]
		req.session['numberTitles'] = len(data)
		for book in data:
			book = searchCatalog(customer, book)
			req.session['count'] += 1

		#refactor 'results' and 'data' into a single variable
		results = data
		matches = 0
		for result in results:
			if result['match'] == "Possible Match":
				matches += 1

		#is session the best way to store these results?
		req.session['results'] = results
		context = {
				'form': form,
				'results' : results,
				'urls' :[customer.url_begin, customer.url_end],
				'search_data': [str(customer.cust_number) + customer.account_suffix, customer.cust_name, len(results), matches]
		}

		return render(req, 'search/results.html', context)

def upload(req):
	if req.method == 'POST':
		form = UploadFileForm(req.POST, req.FILES)
		if form.is_valid():
			#get file from req
			print "Form is valid..."
			uploadedFile = req.FILES['file']
			print "File is uploaded..."
			# first check file extension: if it's not .csv, immediately throw error
			if not str(uploadedFile).lower().endswith(".csv"):
				print "Invalid file extension."
			else:
				# THEN, if file extension is .csv, run the magic typechecker
				# just to make sure that it's really a csv.
				print "File extension valid..."
				typeChecker = magic.from_buffer(uploadedFile.read())
				print typeChecker
				if not 'ASCII text' in typeChecker:
					print "Invalid file type."
				else:
					print "File type valid..."
					req.session['customer_number'] = req.POST['customer_number']
					with open('uploads/wwbsearch.csv', 'wb+') as f:
						for chunk in uploadedFile.chunks():
							f.write(chunk)
					f.close()
	return redirect('/')

def create_file(req):
	if req.POST['filetype'] == 'excel':
		 req.session['filename'] = exportToExcel(req.session['results'], Customer.objects.get(cust_number=req.session['customer_number']))
		 return redirect('/search/export')
	elif req.POST['filetype'] == 'csv':
		print "Coming soon..."
		return HttpResponse(status=204)

def export(req):
	# This route is obviously excessive -- I don't fully understand the routing system, so I've created some
	# sort of bad route that requires this weird path to find my static files...
	return redirect('../../../static/' + req.session['filename'])

def logout(req):
	req.session.flush()
	return redirect('/')