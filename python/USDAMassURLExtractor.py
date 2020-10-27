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

	ingredientText = re.sub('[^-a-zA-Z ]+', '', itemContents[0]).strip().lower()
	ingredientText = ingredientText.replace("  ", " ")
	ingredientText = ingredientText.replace("  ", " ")
	ingredientText = ingredientText.replace("  ", " ")
	recipeWords = ingredientText.split(" ")

	ingredientQuantifiers = itemContents[1][len("Quantifiers:")+1:].strip()
	ingredientNames = itemContents[2][len("Ingredients:")+1:].strip()
	foodGroupCategoriesString = "...Dairy and Egg Products...Spices and Herbs...Fats and Oils...Poultry Products...Soups, Sauces, and Gravies...Sausages and Luncheon Meats...Breakfast Cereals...Fruits and Fruit Juices...Pork Products...Vegetables and Vegetable Products...Nut and Seed Products...Beef Products...Beverages...Finfish and Shellfish Products...Legumes and Legume Products...Lamb, Veal, and Game Products...Baked Products...Sweets...Cereal Grains and Pasta..."

	additionalURLSearchString = ""
	ingredientNameList = ingredientNames.split(" ")

	getURL = "..."
	ingredientName = ""
	baseURL = ""
	for ingredient in ingredientNameList:
		if "_" in ingredient:
			ingredientName = ingredient[:ingredient.find("_")].strip()
		else:
			ingredientName = ingredient.strip()
		for index in range(0,len(recipeWords)):
			if(recipeWords[index] in ingredientName):
				baseURL = "https://ndb.nal.usda.gov/ndb/search/list?manu=none&ds=SR&sort=fd_d&order=asc&qlookup="
				synsets = wordnet.synsets(ingredient)
				for synset in synsets:
					if(not ".n." in synset.name()):
						continue
					synsetTree = []
					additionalURLSearchString = ""
					itemNameString = synset.name()
					itemNameString = itemNameString[:itemNameString.find(".")]
					synsetTree.append(itemNameString)
					hypernyms = synset.hypernyms()
					while(len(hypernyms) > 0):
						hypernym = hypernyms[0]
						itemNameString = hypernym.name()
						itemNameString = itemNameString[:itemNameString.find(".")]
						synsetTree.append(itemNameString)
						hypernyms = hypernym.hypernyms()
					if(len(synsetTree) > 1):
						if("flavorer" in str(synsetTree)):
							baseURL = "https://ndb.nal.usda.gov/ndb/search/list?manu=none&ds=SR&sort=fd_d&order=asc&fgcd=Spices and Herbs&qlookup="
							break
						elif("vegetable" in str(synsetTree)):
							baseURL = "https://ndb.nal.usda.gov/ndb/search/list?manu=none&ds=SR&sort=fd_d&order=asc&fgcd=Vegetables and Vegetable Products&qlookup="
							break
						elif("fruit" in str(synsetTree)):
							baseURL = "https://ndb.nal.usda.gov/ndb/search/list?manu=none&ds=SR&sort=fd_d&order=asc&fgcd=Fruits and Fruit Juices&qlookup="
							break
						elif("dairy" in str(synsetTree)):
							baseURL = "https://ndb.nal.usda.gov/ndb/search/list?manu=none&ds=SR&sort=fd_d&order=asc&fgcd=Dairy and Egg Products&qlookup="
							break
						elif("meat" in str(synsetTree)):
							for itemName in synsetTree:
								if(itemName.lower() in foodGroupCategoriesString.lower()):
									itemNameIndex = foodGroupCategoriesString.lower().find(itemName)
									leftIndex = foodGroupCategoriesString.rfind("...", 0, itemNameIndex)+3
									rightIndex = foodGroupCategoriesString.find("...", itemNameIndex, len(foodGroupCategoriesString))
									categoryString = foodGroupCategoriesString[leftIndex:rightIndex]
									baseURL = "https://ndb.nal.usda.gov/ndb/search/list?manu=none&ds=SR&sort=fd_d&order=asc&fgcd="+categoryString+"&qlookup="
									getURL +=  baseURL
									if(index == 0):
										getURL +=  recipeWords[index]
										if(index+1 < len(recipeWords)):
											getURL +=  "..."+baseURL+recipeWords[index]
											getURL +=  "+"+recipeWords[index+1]
									elif(index == len(recipeWords)-1):
										if(index-1 >= 0):
											getURL +=  recipeWords[index]+"..."+baseURL
											getURL +=  recipeWords[index-1]+"+"
										getURL +=  recipeWords[index]
									else:
										getURL +=  recipeWords[index]+"..."+baseURL
										getURL +=  recipeWords[index-1]+"+"+recipeWords[index]+"..."+baseURL
										getURL +=  recipeWords[index]+"+"+recipeWords[index+1]+"..."+baseURL
										getURL +=  recipeWords[index-1]+"+"+recipeWords[index]+"+"+recipeWords[index+1]
									getURL += "..."
									break
							baseURL = "https://ndb.nal.usda.gov/ndb/search/list?manu=none&ds=SR&sort=fd_d&order=asc&qlookup="
							break
						elif("leaven" in str(synsetTree) or "edible" in str(synsetTree) or "dish" in str(synsetTree) or "food" in str(synsetTree)):
							baseURL = "https://ndb.nal.usda.gov/ndb/search/list?manu=none&ds=SR&sort=fd_d&order=asc&qlookup="
							break
				getURL +=  baseURL
				if(index == 0):
					getURL +=  recipeWords[index]
					if(index+1 < len(recipeWords)):
						getURL +=  "..."+baseURL+recipeWords[index]
						getURL +=  "+"+recipeWords[index+1]
				elif(index == len(recipeWords)-1):
					if(index-1 >= 0):
						getURL +=  recipeWords[index]+"..."+baseURL
						getURL +=  recipeWords[index-1]+"+"
					getURL +=  recipeWords[index]
				else:
					getURL +=  recipeWords[index]+"..."+baseURL
					getURL +=  recipeWords[index-1]+"+"+recipeWords[index]+"..."+baseURL
					getURL +=  recipeWords[index]+"+"+recipeWords[index+1]+"..."+baseURL
					getURL +=  recipeWords[index-1]+"+"+recipeWords[index]+"+"+recipeWords[index+1]
				getURL += "..."
				break
	return getURL


		
	# return getURL
#endGetFirstRecipePage


def extractIngredients():
	#recipeFile = open("recipes/inagarten/Outrageous_Brownies.txt", "r")
	#recipeFile = open("recipes/inagarten/Lemon_Chicken_Breasts.txt", "r")
	recipeFile = open("recipes/inagarten/Chicken_Pot_Pie.txt", "r")
	recipeFileContents = recipeFile.read().strip()
	recipeFile.close()
	ingredientItemList = recipeFileContents.split("\n\n")
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
		outputFile = open("USDAsearchURL.txt", "w")
		for item in nutritionInformationList:
			outputFile.write(item+"\n")
		outputFile.close()
		driver.close()			
		print "finished"
#endMain


main()