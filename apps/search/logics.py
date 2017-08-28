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

	wb.save("static/" + filename)
	return filename

	# TODO:
	#	* save file somewhere in the static directory
	#	* access this file so it gets downloaded to user's computer (use get request? It should function like a link...)

def searchCatalog(self, searchList):
	data = []
	#startTime = time.strftime("%m/%d/%Y %I:%M:%S %p", time.localtime())
	# TODO:
	with open(searchList, 'r') as f:
		reader = csv.reader(f)
		for row in reader:
			if row[0] != '':
				data.append({'item_number': row[0],
					'title': row[1],
					'isbn': row[9],
					'match': ''})

	del data[0]
	num_titles = len(data)
	count = 1
	for book in data:
		print "Checking", book['item_number'], count, "of", num_titles
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