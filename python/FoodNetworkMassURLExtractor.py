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
baseChefURLS = []

def getFirstRecipePage(talentURL):
	global driver, baseChefURLS

	baseChefURLS = []
	outputFilePath = ""
	recipeURLString = ""

	driver.get(talentURL)
	siteContainer = driver.find_element_by_class_name('container-site')
	alphabatizedChefs = siteContainer.find_elements_by_class_name('o-Capsule__m-Body')
	for sameFirstLetterContainer in alphabatizedChefs:
		sameFirstLetterChefs = sameFirstLetterContainer.find_elements_by_class_name('m-PromoList__a-ListItem')
		for chefContainer in sameFirstLetterChefs:
			baseURLText = chefContainer.find_element_by_tag_name("a").get_attribute("href").encode("utf-8").strip()
			baseChefURLS.append(baseURLText)

	for baseURL in baseChefURLS:
		talentTextIndex = baseURL.find("talent/")+len("talent/")
		hostName = baseURL[talentTextIndex:].replace("/", "")
		outputFilePath = "recipes/"+re.sub('[^0-9a-zA-Z ]+', '', hostName)
		if not os.path.exists(outputFilePath):
			os.makedirs(outputFilePath)
		recipeURLString = ""
		pageNo = 1
		driver.get(baseURL+"/recipes/ratings-/p/"+str(pageNo))
		siteContainer = driver.find_element_by_class_name('container-site')
		if("Page Not Found" in siteContainer.text):
			continue
		recipesListContainer = siteContainer.find_element_by_class_name('o-ListRecipe')
		recipeContainers = recipesListContainer.find_elements_by_class_name('m-MediaBlock__a-Headline')
		for recipeContainer in recipeContainers:
			recipeLink = recipeContainer.find_element_by_tag_name("a")
			if(recipeLink is None):
				continue
			recipeAddress = recipeLink.get_attribute("href").encode("utf-8").strip()
			recipeURLString += str(recipeAddress)+"\n"
		outputFile = open(outputFilePath+"/recipeURLs.txt", "w")
		outputFile.write(recipeURLString)
		outputFile.close()
#endGetFirstRecipePage


def main():
	global driver
	try:
		print "starting"
		getFirstRecipePage("http://www.foodnetwork.com/profiles/talent")
	except:
		print "error"
	finally:
		driver.close()
		print "finished"
#endMain


main()