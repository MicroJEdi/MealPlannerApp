#wordnet
from nltk.corpus import wordnet
#selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
#misc
import os
import re

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')  # Last I checked this was necessary.
driver = webdriver.Chrome("chromedriver.exe", chrome_options=options)

def getNutritionInformation(itemContents):
	global driver

	ingredientText = re.sub('[^-a-zA-Z ]+', '', itemContents[1]).strip().lower()
	ingredientText = ingredientText.replace("  ", " ")
	ingredientText = ingredientText.replace("  ", " ")
	ingredientText = ingredientText.replace("  ", " ")
	recipeWords = ingredientText.split(" ")
	for x in range(0,len(recipeWords)):
		if(recipeWords[x].rfind("s") == len(recipeWords[x])-1):
			recipeWords[x] = recipeWords[x][:recipeWords[x].rfind("s")]
	ingredientQuantifiers = itemContents[2][len("Quantifiers:")+1:].strip()
	ingredientNames = itemContents[3][len("Ingredients:")+1:].strip()

	usdaSearchURLs = itemContents[0].split("...")

	maxWordCount = -1
	bestLinkText = "" 
	bestURL = ""
	for usdaURL in usdaSearchURLs:
		if(len(usdaURL.strip()) == 0):
			continue
		searchText = usdaURL[usdaURL.find("&qlookup=")+len("&qlookup="):]
		searchTextWords = searchText.split("+")
		for x in range(0,len(searchTextWords)):
			if(searchTextWords[x].rfind("s") == len(searchTextWords[x])-1):
				searchTextWords[x] = searchTextWords[x][:searchTextWords[x].rfind("s")]
		driver.get(usdaURL)
		try:
			tableDiv = driver.find_element_by_class_name("list-left")
			tableBody = tableDiv.find_element_by_tag_name("tbody")
			rows = tableBody.find_elements_by_tag_name("tr")
			for row in rows:
				columns = row.find_elements_by_tag_name("td")
				linkText = columns[1].find_element_by_tag_name("a").text
				tempWordCount = 0
				for word in searchTextWords:
					if word in linkText:
						tempWordCount += 1
				if(tempWordCount > maxWordCount):
					maxWordCount = tempWordCount
					bestLinkText = columns[1].find_element_by_tag_name("a").text
					bestURL = usdaURL
		except:
			usdaURL = ""


	nutritionInformation = []
	maxWordCount = -1
	bestLink = ""
	linkText = ""
	searchText = bestURL[bestURL.find("&qlookup=")+len("&qlookup="):]
	searchTextWords = searchText.split("+")
	for x in range(0,len(searchTextWords)):
		if(searchTextWords[x].rfind("s") == len(searchTextWords[x])-1):
			searchTextWords[x] = searchTextWords[x][:searchTextWords[x].rfind("s")]

	driver.get(bestURL)
	tableDiv = driver.find_element_by_class_name("list-left")
	tableBody = tableDiv.find_element_by_tag_name("tbody")
	rows = tableBody.find_elements_by_tag_name("tr")
	for row in rows:
		columns = row.find_elements_by_tag_name("td")
		linkText = columns[1].find_element_by_tag_name("a").text
		tempWordCount = 0
		for word in searchTextWords:
			if word in linkText:
				tempWordCount += 1
		if(tempWordCount > maxWordCount):
 			maxWordCount = tempWordCount
 			bestLink = columns[1].find_element_by_tag_name("a")

	nutritionInformation.append(ingredientText)	
	nutritionInformation.append(bestLink.text.strip())
	bestLink.click()
	nutrientDiv = driver.find_element_by_id("nutdata_wrapper")
	headerTable = nutrientDiv.find_element_by_tag_name("table")
	headerTableRows = headerTable.find_elements_by_tag_name("th")

	headerString = ""
	for headerRow in headerTableRows:
		tempString = headerRow.text.strip()
		if(len(tempString) == 0):
			tempString = headerRow.get_attribute('innerHTML')
			tempString = tempString[tempString.find("<br>")+4:].strip()
			tempString = tempString.replace("&nbsp;", " ")
		headerString += tempString+"\n"

	nutritionInformation.append(headerString.strip().replace("\n", "..."))
	nutrientDataTable = nutrientDiv.find_element_by_id("nutdata")
	nutrientDataTableBody = nutrientDataTable.find_element_by_tag_name("tbody")
	nutrientDataTableRows = nutrientDataTableBody.find_elements_by_tag_name("tr")

	count = 0
	for nutrientRow in nutrientDataTableRows:
		tableRowText = nutrientRow.text
		if(len(tableRowText) > 0):
			if(tableRowText.startswith("Energy") or tableRowText.startswith("Carbohydrate") or tableRowText.startswith("Total lipid") or tableRowText.startswith("Protein")):
				columnString = ""
				columns = nutrientRow.find_elements_by_tag_name("td")
				for column in columns:
					columnString += column.text.strip()+"..."
				columnString = columnString[:columnString.rfind("...")]
				nutritionInformation.append(columnString)
				count += 1
			if(count == 4):
				break

	return nutritionInformation
#endGetFirstRecipePage


def extractIngredients():
	#recipeFile = open("recipes/inagarten/Outrageous_Brownies.txt", "r")
	#recipeFile = open("recipes/inagarten/Lemon_Chicken_Breasts.txt", "r")
	usdaLinksFile = open("USDAsearchURL.txt", "r")
	usdaLinksFileContents = usdaLinksFile.read().strip()
	usdaLinksFile.close()
	usdaLinksList = usdaLinksFileContents.split("\n")
	recipeFile = open("recipes/inagarten/Chicken_Pot_Pie.txt", "r")
	recipeFileContents = recipeFile.read().strip()
	recipeFile.close()
	ingredientItemList = recipeFileContents.split("\n\n")
	for x in range(0,len(ingredientItemList)):
		ingredientItemList[x] = usdaLinksList[x] + "\n" + ingredientItemList[x]
	return ingredientItemList
#endExtractIngredients



def main():
	global driver
	nutritionInformationList = []
	try:
		print "starting"	
		ingredientItemList = extractIngredients()
		index = 0
		failedAttempts = 0
		while(index < len(ingredientItemList)):
			try:
				itemContents = ingredientItemList[index].split("\n")
				nutritionInformationList.append(getNutritionInformation(itemContents))
				# usdaSearchURLs = itemContents[0].split("...")
				# for usdaURL in usdaSearchURLs:	
				# 	if(len(usdaURL.strip()) == 0):
				# 		continue
				# 	nutritionInformationList.append(getNutritionInformation(itemContents, usdaURL))
				index += 1
				failedAttempts = 0
			except:
				failedAttempts += 1
				if(failedAttempts > 4):
					index += 1
					failedAttempts = 0
	except:
		print "error"
	finally:
		for item in nutritionInformationList:
			print item[0]
			print item[1]
			print item[2]
			print item[3]
			print item[4]
			print item[5]
			print item[6]+"\n"
		driver.close()			
		print "finished"
#endMain


main()