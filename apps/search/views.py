from django.shortcuts import render, redirect, HttpResponse
from wwb.settings import MEDIA_ROOT, MEDIA_URL
from django.conf import settings
from models import Files, Customer, User
from .forms import UploadFileForm
from logics import exportToExcel


def index(request):
	form = UploadFileForm()
	context = {'form': form,
				'media_root': MEDIA_ROOT}

	return render(request, 'search/index.html', context)

def upload(request):
	if request.method == 'POST':
		form = UploadFileForm(request.POST, request.FILES)
		request.session['customer'] = request.POST['customer']
		if form.is_valid():
			uploaded = request.FILES['file']
			with open('uploads/wwbsearch.csv', 'wb+') as f:
				for chunk in uploaded.chunks():
					f.write(chunk)
			f.close()
			return redirect('search/search_results')
		else:
			return redirect('/')

		

def search_results(request):

	"""

	Will need a lot of error handling. Plenty can go wrong.
	Now that we're actually at the phase where we're scraping the customer's catalog, all the error handling will be done
	"under the hood" - no flash messages, etc. If we encounter any errors, that will be reported in the search results.

	Need to use try/except for this...want script to be able to recover from something unexpected and keep going. If some ISBN
	won't take, move on to the next one.


	"""
	results = Customer.objects.get(cust_number=request.session['customer']).searchCatalog('uploads/wwbsearch.csv')
	request.session['results'] = results

	context = {
	'results' : results,
	'urls' :[Customer.objects.get(cust_number=request.session['customer']).url_begin, Customer.objects.get(cust_number=request.session['customer']).url_end]
	}

	return render(request, 'search/results.html', context)


def export(request):
	if request.POST['filetype'] == 'excel':
		exportToExcel(request.session['results'], request.session['customer'])
	elif request.POST['filetype'] == 'csv':
		print "Coming soon..."

	return HttpResponse(status=204)
