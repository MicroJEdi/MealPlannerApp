# MealPlannerApp
Python WebKrawler scripts for extracting all chef recipes from FoodNetwork.com and estimating the nutritional breakdown for a given recipe's igredient list
### Requirements
* ###### Python 2.7 (https://www.python.org/download/releases/2.7/)
* ###### Selenium & ChromeWebDriver (http://selenium-python.readthedocs.io/)
* ###### NLTK & WordNet (https://www.nltk.org/)
### Python Scripts
* ###### FoodNetworkMassURLExtractor.py (Run First)
  Stores the URLs of every chef's first page of recipes from FoodNetwork.com to be used by MassRecipeExtractor.py
* ###### FoodNetworkMassRecipeExtractor.py (Run Second)
  Stores every item in the recipe's ingredient list with quantifier (amount) and ingredient (food) words identified
* ###### USDAMassURLExtractor.py (Run Third)
  Stores the USDA query URLs for each ingredient list item in the recipe 
* ###### USDAMassNutritionEstimator.py (Run Fourth)
  Stores the estimated nutritional value of every item in the recipe's ingredient list
### TODO
* ###### Cost Estimation
* ###### Mobile Application
### Additional Information
* ###### ChromeWebDriver (https://sites.google.com/a/chromium.org/chromedriver/)
* ###### WordNet Search - 3.1 Online Playground (http://wordnetweb.princeton.edu/perl/webwn)
  
  ![WordNetExample](/images/wordnet.png)
