#Nelson Atkins 41

soup = BeautifulSoup(urlReq.text, "html.parser")
resultsElement = soup.find("h1")
getElementText = resultsText.em.text
# this '0' or whatever will be an attribute we store: the NoResultsText. 
if "0" in ElementText:
	## Do Stuff
	## Mark this one down as Not Found, No Match, No Results, whatever

#Northwestern 5406

soup = BeautifulSoup(html, "html.parser")
resultsElement = soup.find("div", {"id": "resultsNumbersTile"})
getElementText = resultsDiv.h1.em.text
#this header2 is supposed to give the results of a positive search. It can go.
#header2 = soup.find("h2", {"class": "EXLResultTitle"})
if "0" in getElementText:
	# Do Stuff

# 167 Stanford

soup = BeautifulSoup(urlReq.text, "html.parser")
resultsElement = soup.find("div", {"class": "results-heading"})
MatchTest = resultsHeading.h2.text
if "No results found in catalog" in MatchTest:
	# Do stuff