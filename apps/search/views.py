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
			return redirect('/search/execute_search')
		else:
			return redirect('/')


def execute_search(request):
	customer = Customer.objects.get(cust_number=request.session['customer_number'])
	results = searchCatalog(customer, 'uploads/wwbsearch.csv')
	# Up too this point we haven't actually left the "New Search" page. 
	# No new page has been rendered.
	# So set this up to re-render the index page while the search is running,
	# and then redirect to search/search_results when complete.
	# We'll need to break the search functions down into different functions.

	request.session['results'] = results
	return redirect("/search/search_results")

def search_results(request):
	form = UploadFileForm()
	customer = Customer.objects.get(cust_number=request.session['customer_number'])
	results = request.session['results']
	matches = 0
	for result in results:
		if result['match'] == "Possible Match":
			matches += 1


	context = {
			'form': form,
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