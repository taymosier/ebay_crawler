import pprint
import math
import csv
import time
from ebaysdk.finding import Connection as Finding
from ebaysdk.exception import ConnectionError

# This is the main program function, it asks for a search term and a file name, then creates a file and file writer object.
# Next, it calls a function which calls the API and begins the search for current items. Once that function has ran to completion
# it will return the number of items it printed to the file and stores that value in a variable called numberOfCurrentlyListedItems.
# The next line in this function calls the same function but instead searches for previously listed items. It will then return the total
# number of items and store that value in a variable called totalNumberOfItems. It will then terminate the file writer object and print
# the total number of items and the name of the file the data was printed to
def mainFunction(api):
    keyword = input('Enter search keyword: ')
    fileName = input('Enter the name of the file you would like this data written to: ')+'.csv'
    print('')
    with open(fileName, 'w', newline='') as csvfile:
        fieldnames = ['Number', 'Title', 'Price', 'Item ID', 'Global ID', 'Category', 'Payment Method', 'Country', 'Selling State', 'Start Time', 'End Time']
        outputWriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
        outputWriter.writeheader()
        numberOfCurrentlyListedItems = returnResults(0, csvfile, outputWriter, keyword, 'findItemsAdvanced')
        totalNumberOfItems = returnResults(numberOfCurrentlyListedItems, csvfile, outputWriter, keyword, 'findCompletedItems')
        csvfile.close()

    print('Total Items Printed: ' + str(totalNumberOfItems))
    print('Results printed to ' + str(fileName))

# this makes a call to the API in order to determine the total number of items that will be printed in order to know how many items will be Printed
# and how many pages of search results will be returned
def returnResults(itemNumber, outputFile, outputWriter, keyword, searchType):
    response = getInitialResponse(str(searchType), keyword)
    returnedItems = getTotalReturnedItems(response)
    itemNumber = getPages(response, itemNumber, returnedItems, keyword, searchType, outputFile, outputWriter)
    return itemNumber

# this function calls the api using the designated search type and search term as parameters. It then returns the response which will be stored in
# the response variable in the function above [returnResults()]
def getInitialResponse(searchType, keyword):
    response = api.execute(str(searchType), {'keywords': str(keyword)})
    return response

# this function returns the total number of items returned by the search and converts that number to an integer
# it will store this value in the returnedItems variable stored in returnResults()
def getTotalReturnedItems(response):
    returnedItems = int(response.dict()['paginationOutput']['totalEntries'])
    return returnedItems

# This function gets the total number of search result pages and prints how many individual items were returned.
# It then loops through each page and calls the retrievePage function
# If the page is successfully printed, it will print that the page was successfully written to the fileName
# Once the pages are all written to the file, it will return the item number of the last item printed and store it
# in the itemNumber variable contained within the returnResults() function
def getPages(response, itemNumber, returnedItems, keyword, searchType, outputFile, outputWriter):
    totalPages = getTotalNumberOfPages(returnedItems)
    printNumberOfItems(returnedItems, searchType)
    for i in range(totalPages):
        time.sleep(.2)
        itemNumber = retrievePage(i, itemNumber, searchType, keyword, totalPages, outputFile, outputWriter)
        print('Page [' + str(i+1) + '/' + str(totalPages) + '] successfully written to file')
    return itemNumber

# Since there can only be a maximum number of 100 items per page, this function gets the total number of pages by
# dividing the total number of items by 100 and rounding up, so that if there were 4340 results returned, it would
# be a total of 44 pages. It then returns the number of pages and stores it in the totalPages variable contained in
# the getPages() function
def getTotalNumberOfPages(returnedItems):
    totalPages = math.ceil(returnedItems/100)
    return totalPages

# This function prints out how many items are being printed. It prints out different messages depending on whether or not
# it is searching for currently or previously listed items
def printNumberOfItems(returnedItems, searchType):
    if searchType == 'findItemsAdvanced':
        print('Printing ' + str(returnedItems) + ' Currently Listed Items')
    elif searchType == 'findCompletedItems':
        print('')
        print('Printing ' + str(returnedItems) + ' Previously Listed Items')

# this is the function called in the getPages() function loop. It makes a call to the API for the page number equal to
# the current loop, so that if the loop is on its second cycle it will request the data on page two of the search results.
# The itemNumber variable is updated each time an itemNumber is written to the file. It will then return this value to the
# itemNumber variable contained within the loop of the getPages() function
def retrievePage(i, itemNumber, searchType, keyword, totalPages, outputFile, outputWriter):
    response = makeAPICall(i, searchType, keyword, totalPages)
    itemNumber = writeItemsOnPageToFile(response, itemNumber, totalPages, outputFile, outputWriter)
    return itemNumber

# This is the function that makes the API call for a specific page. Once the page result is retrieved, it is
# returned and stored in the response variable in the retrievePage() function. The data within that variable is then
# injected into the writeItemsOnPageToFile() function as a parameter
def makeAPICall(i, searchType, keyword, totalPages):
    requestCompleted = False
    print('')
    while(requestCompleted == False):
        try:
            response = api.execute(str(searchType), {
            'keywords': str(keyword),
            'paginationInput': {
            'entriesPerPage': '100',
            'pageNumber': str(i+1)
            }
            })
        except:
            print('API Request Failed. Reattempting in 2 seconds')
            time.sleep(2)
            pass
        else:
            requestCompleted == True
            print('API Successfully Requested Page [' + str(i+1) + '/' + str(totalPages) + ']')
            return response

# This is the function that loops through each item on the page and updates the current item number
# it loops through each item and writes it to the file through th writeItemToFile() function
def writeItemsOnPageToFile(response, itemNumber, totalPages, outputFile, outputWriter):
    for item in response.dict()['searchResult']['item']:
        itemNumber = int(itemNumber+1)
        writeItemToFile(item, itemNumber, outputFile, outputWriter)
    return itemNumber

# This function is what writes the information to the file. It pulls each relevant piece of data and
# stores those values in their own separate variable. It then writes those values to the appropriate column
# in the file. If an item has a special character in the title, it will cause an error and the program will
# print that the item was not written to the file
def writeItemToFile(item, itemNumber, outputFile, outputWriter):
    itemTitle = str(item['title'])
    itemPrice = float(item['sellingStatus']['convertedCurrentPrice']['value'])
    itemID = str(item['itemId'])
    globalID = str(item['globalId'])
    categoryName = str(item['primaryCategory']['categoryName'])
    itemPaymentMethod = str(item['paymentMethod'])
    # TODO return only the country, remove city/state
    itemCountry = str(item['location'])
    itemSellingState = str(item['sellingStatus']['sellingState'])
    itemStartTime = splitDate(str(item['listingInfo']['startTime']))
    itemEndTime = splitDate(str(item['listingInfo']['endTime']))
    try:
        outputWriter.writerow(
        {
        'Number': itemNumber,
        'Title': itemTitle,
        'Price': itemPrice,
        'Item ID': itemID,
        'Global ID': globalID,
        'Category': categoryName,
        'Payment Method': itemPaymentMethod,
        'Country': itemCountry,
        'Selling State': itemSellingState,
        'Start Time': itemStartTime,
        'End Time': itemEndTime
        })
    except:
        print("Item number: " + str(itemNumber) + " failed to be written to file")

# This date and time of each item is returned in a format that requires the date and time to be separated.
# This function does that and returns the date in a yyyy-mm-dd function. It will appear in the reverse order when
# the file is opened in excel
def splitDate(time):
    date = str(time)
    dateSplit = date.split('-')
    year = str(dateSplit[0])
    month = str(dateSplit[1])
    day = dateSplit[2].split('T')[0]
    date = str(year + '-' + month + '-' + day)
    return date



# The api varibale makes the initial API call and its value is inserted into the mainFunction() as a parameter
api = Finding(appid='TaylorMo-PythonEB-PRD-e5d865283-1005e2c5', config_file=None)
# This is what calls the main function and begins the chain of events for the script
mainFunction(api)
