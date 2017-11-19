import openpyxl
import requests, time
from bs4 import BeautifulSoup
from datetime import datetime

def exportToExcel(data, customer):


	wb = openpyxl.Workbook()
	ws = wb.active
	ws.title = "Search results"

	ws.append(["Item Number", "Title", "ISBN", "Search Results"])

	for book in data:
		link = "=HYPERLINK(\"" + customer.url_begin + "\"&" + book['isbn'] +"&\""+ customer.url_end +"\", \""+ book['match'] +"\")"
		row = [book['item_number'], book['title'], book['isbn'], link]
		ws.append(row)
	
	for row in range(2, len(data) + 2):
		cell = "D" + str(row)
		ws[cell].style = "Hyperlink"

	search_date = datetime.strftime(datetime.now(), "%m%d%Y")
	filename = str(customer.cust_number) + "search_results" + search_date + '.xlsx'

	wb.save("static/" + filename)
	return filename

	# TODO:
	#	* save file somewhere in the static directory
	#	* access this file so it gets downloaded to user's computer (use get request? It should function like a link...)

def searchCatalog(customer, book):

	#startTime = time.strftime("%m/%d/%Y %I:%M:%S %p", time.localtime())
	book['isbn'] = book['isbn'].replace("ISBN ", "")
	url = customer.url_begin + book['isbn'] + customer.url_end
	urlReq = requests.get(url)
	soup = BeautifulSoup(urlReq.text, 'html.parser')
	elem_list = customer.element.split(',')
	parse_element = soup.find(elem_list[0], {elem_list[1]:elem_list[2]})
	if customer.catalog_type == "B":
		if customer.keywords in parse_element.text:
			book['match'] = "No Match"
		else:
			book['match'] = "Possible Match"
	else:
		if parse_element != None:
			book['match'] = "No Match"
		else:
			book['match'] = "Possible Match"

	return book