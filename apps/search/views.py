from django.shortcuts import render, redirect, HttpResponse
from wwb.settings import MEDIA_ROOT, MEDIA_URL
from django.conf import settings
from models import Files, Customer, User
from .forms import UploadFileForm
from logics import exportToExcel, searchCatalog


def index(request):
	form = UploadFileForm()
	context = {'form': form,
				'media_root': MEDIA_ROOT}

	return render(request, 'search/index.html', context)

def upload(request):
	if request.method == 'POST':
		form = UploadFileForm(request.POST, request.FILES)
		request.session['customer_number'] = request.POST['customer_number']
		if form.is_valid():
			uploaded = request.FILES['file']
			with open('uploads/wwbsearch.csv', 'wb+') as f:
				for chunk in uploaded.chunks():
					f.write(chunk)
			f.close()
			return redirect('/search/search_results')
		else:
			return redirect('/')


	"""

	Will need a lot of error handling. Plenty can go wrong.
	Now that we're actually at the phase where we're scraping the customer's catalog, all the error handling will be done
	"under the hood" - no flash messages, etc. If we encounter any errors, that will be reported in the search results.

	Need to use try/except for this...want script to be able to recover from something unexpected and keep going. If some ISBN
	won't take, move on to the next one.


	"""
	# Do I need a results variable or could I just store it all in session?	

def search_results(request):


	customer = Customer.objects.get(cust_number=request.session['customer_number'])
	results = searchCatalog(customer, 'uploads/wwbsearch.csv')
	request.session['results'] = results
	matches = 0
	for result in results:
		if result['match'] == "Possible Match":
			matches += 1


	context = {
			'results' : results,
			'urls' :[customer.url_begin, customer.url_end],
			'search_data': [str(customer.cust_number) + customer.account_suffix, customer.cust_name, len(results), matches]
	}

	return render(request, 'search/results.html', context)


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