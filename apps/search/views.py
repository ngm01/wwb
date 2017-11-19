from django.shortcuts import render, redirect, HttpResponse
from wwb.settings import MEDIA_ROOT, MEDIA_URL
from django.conf import settings
from models import Files, Customer, User
from .forms import UploadFileForm
from logics import exportToExcel, searchCatalog
import csv, magic, io


def index(request):
	form = UploadFileForm()
	# Checks whether there is a customer number saved in session -
	# this functions as a check whether a search has been executed or not.
	if 'customer_number' not in request.session:
		context = {'form': form,
					'media_root': MEDIA_ROOT}

		return render(request, 'search/index.html', context)
	
	else:
		customer = Customer.objects.get(cust_number=request.session['customer_number'])
		
		data = []
		request.session['count'] = 0;

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
		request.session['numberTitles'] = len(data)
		for book in data:
			book = searchCatalog(customer, book)
			request.session['count'] += 1

		#refactor 'results' and 'data' into a single variable
		results = data
		matches = 0
		for result in results:
			if result['match'] == "Possible Match":
				matches += 1

		#is session the best way to store these results?
		request.session['results'] = results
		context = {
				'form': form,
				'results' : results,
				'urls' :[customer.url_begin, customer.url_end],
				'search_data': [str(customer.cust_number) + customer.account_suffix, customer.cust_name, len(results), matches]
		}

		return render(request, 'search/results.html', context)

def upload(request):
	if request.method == 'POST':
		form = UploadFileForm(request.POST, request.FILES)
		if form.is_valid():
			#get file from request
			uploadedFile = request.FILES['file']
			#create magic type checker
			typeChecker = magic.from_buffer(uploadedFile.read())
			print typeChecker
			if not 'ASCII text' in typeChecker:
				print "invalid file type"
			else:
				request.session['customer_number'] = request.POST['customer_number']
				with open('uploads/wwbsearch.csv', 'wb+') as f:
					for chunk in uploadedFile.chunks():
						f.write(chunk)
				f.close()
	return redirect('/')

def create_file(request):
	if request.POST['filetype'] == 'excel':
		 request.session['filename'] = exportToExcel(request.session['results'], Customer.objects.get(cust_number=request.session['customer_number']))
		 return redirect('/search/export')
	elif request.POST['filetype'] == 'csv':
		print "Coming soon..."
		return HttpResponse(status=204)

def export(request):
	# This route is obviously excessive -- I don't fully understand the url routing system, so I've created some
	# sort of bad route that requires this weird path to find my static files.
	return redirect('../../../static/' + request.session['filename'])

def logout(request):
	request.session.flush()
	return redirect('/')