#wordnet
from nltk.corpus import wordnet
#selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
#misc
import os
import re
import glob


def buildHypernymTrees(lines, chefFolder):
	
	host = chefFolder[chefFolder.find("recipes\\")+len("recipes\\"):]
	print host

	options = Options()
	options.add_argument('--headless')
	options.add_argument('--disable-gpu')
	driver = webdriver.Chrome(chrome_options=options)

	for recipeURL in lines:
		if(len(recipeURL.strip()) > 0):
			outputFileText = ""
			driver.get(recipeURL.strip())
			siteContainer = driver.find_element_by_class_name('container-site')
			recipeName = siteContainer.find_element_by_class_name('o-AssetTitle__a-Headline').text.strip()
			outputFileName = chefFolder+"\\"+re.sub('[^0-9a-zA-Z ]+', '', recipeName)+".txt"
			outputFileName = outputFileName.replace(" ","_")
			if(os.path.isfile(outputFileName)):
				continue
			recipeIngredients = siteContainer.find_element_by_class_name('o-Ingredients__m-Body').text.strip()
			ingredients = str(recipeIngredients).split("\n")
			for ingredient in ingredients:
				words = re.sub('[^-0-9a-zA-Z/ ]+', '', ingredient).split(" ")
				name = ""
				quantifier = ""
				for x in range(0, len(words)):
					word = words[x].strip()
					if("/" in word):
						values = word.split('/')
						if(len(values) == 2 and values[0].isdigit() and values[1].isdigit()):
							quantifier += word + " "
							continue
					synsets = wordnet.synsets(word)
					doBreak = False
					for synset in synsets:
						if(not ".n." in synset.name()):
							continue
						synsetTree = []
						synsetTree.append(synset)
						hypernyms = synset.hypernyms()
						while(len(hypernyms) > 0):
							hypernym = hypernyms[0]
							synsetTree.append(hypernym)
							hypernyms = hypernym.hypernyms()
						if(len(synsetTree) > 1):
							if("instrumentality" in str(synsetTree) or "measure" in str(synsetTree)):
								if("_"+words[x] not in quantifier):
									quantifier += word + " "
								doBreak = True
							if("leaven" in str(synsetTree) or "edible" in str(synsetTree) or "fruit" in str(synsetTree) or "vegetable" in str(synsetTree) or "food" in str(synsetTree)):
								if("_"+words[x] not in name):
									name += word + " "
								doBreak = True
							if(doBreak == True):
								break
					if(x < len(words)-1):
						word += "_"+words[x+1].strip()
						synsets = wordnet.synsets(word)
						doBreak = False
						for synset in synsets:
							if(not ".n." in synset.name()):
								continue
							synsetTree = []
							synsetTree.append(synset)
							hypernyms = synset.hypernyms()
							while(len(hypernyms) > 0):
								hypernym = hypernyms[0]
								synsetTree.append(hypernym)
								hypernyms = hypernym.hypernyms()
							if(len(synsetTree) > 1):
								if("instrumentality" in str(synsetTree) or "measure" in str(synsetTree)):
									if(words[x] in quantifier):
										quantifier = quantifier.replace(words[x]+" ", "")
									if(words[x] in name):
										name = name.replace(words[x]+" ", "")
									quantifier += word + " "
									doBreak = True
								if("leaven" in str(synsetTree) or "edible" in str(synsetTree) or "fruit" in str(synsetTree) or "vegetable" in str(synsetTree) or "food" in str(synsetTree)):
									if(words[x] in name):
										name = name.replace(words[x]+" ", "")
									if(words[x] in quantifier):
										quantifier = quantifier.replace(words[x]+" ", "")
									name += word + " "
									doBreak = True
								if(doBreak == True):
									break
				outputFileText += str(ingredient)
				outputFileText += "\nQuantifiers: "+str(quantifier)
				outputFileText += "\nIngredients: "+str(name)+"\n\n"
			outputFile = open(outputFileName, "w")
			outputFile.write(outputFileText)
	driver.stop_client()
	driver.quit()
#endBuildHypernymTrees


def main():
	dirlist = glob.glob('recipes\\*')	
	previousChefFirstName = "warren"#"ted"#"nigella"#"chris"
	previousChefLastName = "brown"#"allen"#"lawson"# "santos"
	previousChefFound = True
	for chefFolder in dirlist:
		if(not previousChefFound and previousChefFirstName in chefFolder.lower() and previousChefLastName in chefFolder.lower()):
			previousChefFound = True
			continue
		elif(not previousChefFound):
			continue
		chefFolder = chefFolder.strip()
		recipeFileName = chefFolder+"\\recipeURLs.txt"
		outputFileName = ""
		if(os.path.isfile(recipeFileName)):
			inputFile = open(recipeFileName, "r")
			lines = inputFile.read().split("\n")
			inputFile.close()
			buildHypernymTrees(lines, chefFolder)
#endMain


main()