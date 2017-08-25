import openpyxl
from datetime import datetime

def exportToExcel(data, customer):

	wb = openpyxl.Workbook()
	ws = wb.active	
	ws.title = "Search results"

	ws.append(["Item Number", "Title", "ISBN", "Search Results"])

	for book in data:
		row = [book['item_number'], book['title'], book['isbn'], book['match']]
		ws.append(row)
	
	search_date = datetime.strftime(datetime.now(), "%m%d%Y")
	filename = customer + "search_results" + search_date + '.xlsx'

	# TODO:
	#	* save file somewhere in the static directory
	#	* access this file so it gets downloaded to user's computer (use get request? It should function like a link...)

	wb.save(filename)
