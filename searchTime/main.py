import requests
import time
import csv
import os

# Importing path from pathlib in order to read the CSV file 
from pathlib import Path

# These variables store the URL and API Key which allow for me to get information from NYT
apiUrl='https://api.nytimes.com/svc/search/v2/articlesearch.json?'
apiKey='5BFYoDLOoRT9inbABcsaoJAPzT5A7zUBFvYU47LKmE4MFGGX'

# This is a class for a search instance
class Search:
    
        # This variable contains a dictionary for the search parameters.
        params = {'q': 'skateboarding', 
        'api-key': apiKey,
        'fq': 'typeOfMaterials:"News"', 
        'begin_date': '20250101', 
        'end_date': '20250201', 
        'page': 0}
        
        # This initializes a search object
        def __init__(self):
                self.params = self.params

        # GETTER METHODS

        def getQuery(self):
                return self.params['q']

        def getBeginDate(self):
                return self.params['begin_date']

        def getEndDate(self):
                return self.params['end_date']
        
        def getPageNum(self):
                return self.params['page']

        # Here I am defining a method to get the number of pages returned from the call
        def getPageCount(self):

                # Here the api is called and a response is stored in json format
                response = requests.get(apiUrl,params=self.params).json()

                # This formula returns the pages since each page store 10 results
                return response['response']['metadata']['hits'] // 10 + 1

        # Here I am defining a method to get page hits
        def getPageHits(self):

                # Here the api is called and a response is stored in json format
                response = requests.get(apiUrl,params=self.params).json()

                # This navigates through the dictionaries in the data to return a response
                return response['response']['metadata']['hits']
        
        # Here I am defining a method to get page results 
        def getPageData(self):
                # Here the api is called and a response is stored in json format
                response = requests.get(apiUrl,params=self.params).json()

                # This returns the entire response
                return response['response']

        # Here I am defining a method to view the names of the articles on the page
        def getArticleNames(self):

                # Here the api is called and a response is stored in json format
                response = requests.get(apiUrl,params=self.params).json()

                # This variable will be the output string
                output = ''

                # A for loop is used to navigate through the dictionary that contains names
                for article in response['response']['docs']:

                        # Each headline is added to the output
                        output = f"{output}{article['headline']['main']}\n"

                return output

        # Returns a list with all the page's subjects
        def getPageSubjects(self):
                # Here the api is called and a response is stored in json format
                response = requests.get(apiUrl,params=self.params).json()


                # This list will be useful for keeping track of keyword subjects
                subjectList = []

                # This variable stores the entire dictionary within the keywords
                keywords = response['response']['docs'][0]['keywords']

                # A for loop is used to navigate through the dictionary that contains keywords
                for keyword in keywords:

                        # This stores the subject name of the keyword
                        subject = keyword['name']

                        # If a subject is not present within the subject list, add it to the list
                        if subject not in subjectList:
                                subjectList.append(subject)

                return subjectList

        # Here I am defining a method to view the keywords that show up within a given subject
        def getKeywordsBySubject(self, subject):

                # Here the api is called and a response is stored in json format
                response = requests.get(apiUrl,params=self.params).json()

                # This variable stores the entire dictionary with the keywords
                keywords = response['response']['docs'][0]['keywords']

                # This variable will be the output string
                output = '\n'

                # A for loop is used to navigate through the dictionary that contains keywords
                for keyword in keywords:

                        # if the subject of a keyword is equal to the one the user provided, add its value to the output
                        if subject == keyword['name']:
                                output = f"{output}{keyword['value']}\n"

                return output

        # Here I am definind a method to retun the section count of the current page
        def getPageSectionCount(self):
                # This dictionary will store each sections and its count throughout the data
                sectionCountDict = {}

                # Does a new call to the api
                response = requests.get(apiUrl,params=self.params).json()

                # Iterates through each article in the page
                for article in response['response']['docs']:

                        # Stores the section name of the article
                        sectionName = article['section_name']
                
                        # If the name is not stored within the count dictionary, add it with a value of 1
                        if not sectionCountDict.get(sectionName):
                                sectionCountDict[sectionName] = 1
                        # If the name is present within the dictionary, add 1 to its count
                        else:
                                sectionCountDict[sectionName] += 1

                return sectionCountDict

        # Here I am defining a method to view the subjects present throughout all pages
        def getAllPageSubjects(self):
                # Here the api is called and a response is stored in json format
                response = requests.get(apiUrl,params=self.params).json()

                # This list will be useful for keeping track of keyword subjects
                subjectList = []

                # Iterates through each page
                for i in range(response['response']['metadata']['hits'] // 10 + 1):

                        # Showcases to the user which page is being run
                        print(f"Now running page {i}")

                        # Changes the page number based on the current index 
                        self.params['page'] = i

                        # Does a new call to the api
                        response = requests.get(apiUrl,params=self.params).json()

                        # This variable stores the entire dictionary within the keywords
                        keywords = response['response']['docs'][0]['keywords']

                        # A for loop is used to navigate through the dictionary that contains keywords
                        for keyword in keywords:

                                # This stores the subject name of the keyword
                                subject = keyword['name']

                                # If a subject is not present within the subject list, add it to the list
                                if subject not in subjectList:
                                        subjectList.append(subject)

                        # This provides a time buffer to prevent the api from blocking my calls
                        time.sleep(15)
                
                return subjectList

        # Here I am defining a method to view the keyword count by subject throughout all pages
        def getAllPageKeywordsBySubject(self, subject):

                # Here the api is called and a response is stored in json format
                response = requests.get(apiUrl,params=self.params).json()

                # This list will be useful for keeping track of keywords
                keywordCountDict = {}

                # Iterates through each page
                for i in range(response['response']['metadata']['hits'] // 10 + 1):

                        # Showcases to the user which page is being run
                        print(f"Now running page {i}")

                        # Changes the page number based on the current index 
                        self.params['page'] = i

                        # Does a new call to the api
                        response = requests.get(apiUrl,params=self.params).json()

                        # This variable stores the entire dictionary within the keywords
                        keywords = response['response']['docs'][0]['keywords']

                        # A for loop is used to navigate through the dictionary that contains keywords
                        for keyword in keywords:

                                # This stores the subject name of the keyword
                                if subject == keyword['name']:
                                        if not keywordCountDict.get(keyword['value']):
                                                keywordCountDict[keyword['value']] = 1
                                        else:
                                                keywordCountDict[keyword['value']] += 1

                        # This provides a time buffer to prevent the api from blocking my calls
                        time.sleep(15)
                
                return keywordCountDict
        
        # Here I am determining the count of each section within the data
        def getAllPageSectionCount(self):
                
                # This dictionary will store each sections and its count throughout the data
                sectionCountDict = {}

                # Does a call to the api to help initiate the for loop
                response = requests.get(apiUrl,params=self.params).json()

                # The for loop will loop once for each page
                for i in range(response['response']['metadata']['hits'] // 10 + 1):

                        # Showcases to the user which page is being run
                        print(f"Now running page {i}")

                        # Changes the page number based on the current index 
                        self.params['page'] = i

                        # Does a new call to the api
                        response = requests.get(apiUrl,params=self.params).json()

                        # Iterates through each article in the page
                        for article in response['response']['docs']:

                                # Stores the section name of the article
                                sectionName = article['section_name']
                        
                                # If the name is not stored within the count dictionary, add it with a value of 1
                                if not sectionCountDict.get(sectionName):
                                        sectionCountDict[sectionName] = 1
                                # If the name is present within the dictionary, add 1 to its count
                                else:
                                        sectionCountDict[sectionName] += 1
                        
                        # This provides a time buffer to prevent the api from blocking my calls
                        time.sleep(15)
                
                return sectionCountDict
        
        # SETTER METHODS

        def setQuery(self, newQuery):
                # Setting the query value to the given parameter
                self.params['q'] = newQuery

        def setBeginDate(self, newBeginDate):
                # Setting the beginDate value to the given parameter
                self.params['begin_date'] = newBeginDate

        def setEndDate(self, newEndDate):
                # Setting the endDate value to the given parameter
                self.params['end_date'] = newEndDate

        def setPageNum(self, newPageNum):
                        # Setting the Page Number value to the given parameter
                        self.params['page'] = newPageNum

        # This returns the search parameters being used
        def __str__(self):
                
                # {'q': 'skateboarding', 'api-key': apiKey, 'fq': 'typeOfMaterials:"News"', 'begin_date': '20250101', 'end_date': '20260511', 'page': 0}
                return f"""Current Instance:
Section: {self.params["fq"].split(":",1)[1].strip('"')}
Query: {self.params["q"].title()}
Begin Date: {self.params["begin_date"]}
End Date: {self.params["end_date"]}
Page: {self.params["page"]}
"""

# Helper Methods

# A method that allows for the user to update a string parameter
def updateStringParam(parameter, getter, setter):

        # Ask user for the query they'd like
        query = input(f"Which {parameter} would you like to use?: ")

        # Check input, if it is invalid tell the user, else set it to the query value
        if not query:
                return f"Invalid {parameter}"
        
        setter(query)
        return f"New {parameter}: {getter().title()}\n"

# A method that allows for the user to update an integer parameter
def updateIntParam(parameter, getter, setter):

        # Ask user for the value they'd like
        value = input(f"Which {parameter} would you like to use?: ")

        # Check input, if it is not an int tell the user, else set it to the value
        try:
                int(value)
        except ValueError:
                return f"Invalid {parameter}"

        setter(value)
        return f"New {parameter}: {getter()}\n"

# Here is a method that will output a list in a nicely formatted string
def formatListToString(list):

        # This is the output string
        output = ""

        # Keeps track of the number of items in the list
        count = 0

        # Iterates through each item in the list
        for item in list:
                count += 1 # Adds to the count
                output += f"{count}. {item}\n" # Format (1. Item, etc.)

        return output

# Here is a method that will output a dictionary in a nicely formatted string
def formatDictToString(dict):
        # This is the output string
        output = ""

        count = 0
        
        # Iterates through each item in the list
        for key, value in dict.items():
                count += 1 # Adds to the count
                output += f"{count}. {key}: {value}\n" # Format (1. Item, etc.)
        
        return output

# Here I am defining a function that formats dictionaries for adding it to a csv file
def formatCountsForCSV(dict):

        # This is the list that will be outputted by the function
        listOfCounts = []

        # Iterates through each key value pair in the input dictionary
        for k,v in dict.items():
                
                # Creates a temporary dictionary for the key value pair
                tempDict = {}

                # Sets the key and value to their appropriate keys within the temporary dictionary
                tempDict['Value'] = k
                tempDict['Count'] = v

                # Adds the temporary dictionary to the list
                listOfCounts.append(tempDict)

        # Returns a list populated with dictionaries that contains the keys and counts
        return listOfCounts

# Here I am defining a function that outputs a comma seperated list into a csv file 
def outputFile(listOfCounts):
        
        # Finds the file path to the current directory using the OS library
        currDir = os.path.dirname(os.path.abspath(__file__))
        
        # Sets a file path to a data.csv file which will serve as the output file. 
        filePath = os.path.join(currDir, 'data.csv')

        # Opens the data.csv file
        with open(filePath, mode='w', newline='') as file:

                # Sets the names of the fields
                fieldnames = ['Value', 'Count']

                # Initializes an object that will write to the csv file
                writer = csv.DictWriter(file,fieldnames=fieldnames)

                # Writes the header and each row of the file
                writer.writeheader()
                writer.writerows(listOfCounts)
        
        print(f'Done!\n')

instance = Search()
print("\nWelcome to Amauris' NYT API Interface\n")

# User Interface Using An Infinite Loop

while(True):
        task = input("""Choose a task:
[0] Help
[1] Show Search Instance
-----------------------------------------
[2] Change All Search Parameters
[3] Change Query
[4] Change Begin Date
[5] Change End Date
[6] Change Page Number
-----------------------------------------
[7] Get Number of Hits
[8] Get Page Response Data
[9] Get Article Names
[10] Get Current Page Subjects
[11] Get Current Page Keywords by Subject
[12] Get Current Page Section Count
[13] Get All Page Subjects
[14] Get All Page Section Counts
-----------------------------------------
[15] Load All Page Keyword by Subject Count
[16] Load All Page Section Count Data To CSV

[.] Exit
\n""")
        
        print()

        if task == '.':
                break
        elif task == '0':
                print("""In order to use this program, enter a valid number from the list and press enter
Type . and press enter to exit
""")
        elif task == '1': 

                print(instance)

        elif task == '2':

                print(instance)
                print(updateStringParam("Query", instance.getQuery, instance.setQuery))
                print(updateIntParam("Begin Date", instance.getBeginDate, instance.setBeginDate))
                print(updateIntParam("End Date", instance.getEndDate, instance.setEndDate))
                print(updateIntParam("Page Number", instance.getPageNum, instance.setPageNum))
                print(instance)

        elif task == '3':

                print(instance)
                print(updateStringParam("Query", instance.getQuery, instance.setQuery))
                
        elif task == '4':

                print(instance)
                print(updateIntParam("Begin Date", instance.getBeginDate, instance.setBeginDate))

        elif task == "5":

                print(instance)
                print(updateIntParam("End Date", instance.getEndDate, instance.setEndDate))

        elif task == "6":

                print(instance)
                print(updateIntParam("Page Number", instance.getPageNum, instance.setPageNum))

        elif task == "7":

                print(instance)
                print(f"Number of Hits: {instance.getPageHits()}\n")

        elif task == "8":

                print(instance)
                print(f"API Dictionary: {instance.getPageData()}\n")

        elif task == "9":

                print(instance)
                print(instance.getArticleNames())

        elif task == "10":

                print(instance)
                print(formatListToString(instance.getPageSubjects()))

        elif task == "11":

                print(instance)
                print(formatListToString(instance.getPageSubjects()))
                # Here the user will input which subject they are going to use
                subject = input(f"Choose from the subjects above: ").title()
        
                print(instance.getKeywordsBySubject(subject))

        elif task == "12":

                print(instance)
                print(formatDictToString(instance.getPageSectionCount()))

        elif task == "13":

                print(instance)
                list = instance.getAllPageSubjects()
                print(formatListToString(instance.getAllPageSubjects()))

        elif task == "14":

                print(instance)
                print(instance.getAllPageSectionCount())

        elif task == "15":

                print(instance)
                print(formatListToString(instance.getPageSubjects()))
                # Here the user will input which subject they are going to use
                subject = input(f"Choose from the subjects above: ").title()

                output = outputFile(formatCountsForCSV(instance.getAllPageKeywordsBySubject(subject)))

        elif task == "16":
        
                print(instance)
                output = outputFile(formatCountsForCSV(instance.getAllPageSectionCount()))

        


        