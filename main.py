import pprint
import math
import csv
import time
from ebaysdk.finding import Connection as Finding
from ebaysdk.exception import ConnectionError

def returnResults(itemNumber, outputFile, outputWriter, keyword, searchType):
    response = getInitialResponse(str(searchType), keyword)
    returnedItems = getTotalReturnedItems(response)
    itemNumber = getPages(response, itemNumber, returnedItems, keyword, searchType, outputFile, outputWriter)
    return itemNumber


def getInitialResponse(searchType, keyword):
    response = api.execute(str(searchType), {'keywords': str(keyword)})
    return response


def getTotalReturnedItems(response):
    returnedItems = int(response.dict()['paginationOutput']['totalEntries'])
    return returnedItems


def getPages(response, itemNumber, returnedItems, keyword, searchType, outputFile, outputWriter):
    totalPages = math.ceil(returnedItems/100)
    printNumberOfItems(returnedItems, searchType)
    for i in range(totalPages):
        time.sleep(.2)
        itemNumber = retrievePage(i, itemNumber, searchType, keyword, totalPages, outputFile, outputWriter)
        print('Page [' + str(i+1) + '/' + str(totalPages) + '] successfully written to file')
    return itemNumber


def printNumberOfItems(returnedItems, searchType):
    if searchType == 'findItemsAdvanced':
        print('Printing ' + str(returnedItems) + ' Currently Listed Items')
    elif searchType == 'findCompletedItems':
        print('Printing ' + str(returnedItems) + ' Previously Listed Items')


def retrievePage(i, itemNumber, searchType, keyword, totalPages, outputFile, outputWriter):
    response = makeAPICall(i, searchType, keyword, totalPages)
    itemNumber = writeItemsOnPageToFile(response, itemNumber, totalPages, outputFile, outputWriter)
    return itemNumber


def makeAPICall(i, searchType, keyword, totalPages):
    requestCompleted = False
    print('')
    while(requestCompleted == False):
        try:
            response = api.execute(str(searchType), {
            'keywords': str(keyword),
            'paginationInput': {
            'entriesPerPage': 100,
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


def writeItemsOnPageToFile(response, itemNumber, totalPages, outputFile, outputWriter):
    for item in response.dict()['searchResult']['item']:
        itemNumber = int(itemNumber+1)
        writeItemToFile(item, itemNumber, outputFile, outputWriter)
    return itemNumber


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
        print("Item number: " + str(itemNumber) + " failed to print")


def splitDate(time):
    date = str(time)
    dateSplit = date.split('-')
    year = str(dateSplit[0])
    month = str(dateSplit[1])
    day = dateSplit[2].split('T')[0]
    date = str(year + '-' + month + '-' + day)
    return date

def mainFunction(api):
    keyword = input('Enter search keyword: ')
    fileName = input('Enter the name of the file you would like this data written to: ')+'.csv'
    print('')
    with open(fileName, 'w', newline='') as csvfile:
        fieldnames = ['Number', 'Title', 'Price', 'Item ID', 'Global ID', 'Category', 'Payment Method', 'Country', 'Selling State', 'Start Time', 'End Time']
        outputWriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
        outputWriter.writeheader()
        itemNumber = returnResults(0, csvfile, outputWriter, keyword, 'findItemsAdvanced')
        itemNumber = returnResults(itemNumber, csvfile, outputWriter, keyword, 'findCompletedItems')
        csvfile.close()

    print('Total Items Printed: ' + str(itemNumber))
    print('Results printed to ' + str(fileName))


api = Finding(appid='TaylorMo-PythonEB-PRD-e5d865283-1005e2c5', config_file=None)
mainFunction(api)
