import pprint
import math
import csv
import time
from ebaysdk.finding import Connection as Finding
from ebaysdk.exception import ConnectionError

def makefindAdvancedItemsAPICall(i):
    requestCompleted = False
    print('')
    while(requestCompleted == False):
        try:
            response = api.execute('findItemsAdvanced', {
            'keywords': 'Cracker Barrel',
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
            print('API Request Success')
            return response


def makeFindCompletedItemsAPICall(i):
    requestCompleted = False
    print('')
    while(requestCompleted == False):
        try:
            response = api.execute('findCompletedItems', {
            'keywords': 'Cracker Barrel',
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
            print('API Request Success')
            return response


def getInitialResponse(searchType, keyword):
    response = api.execute(str(searchType), {'keywords': str(keyword)})
    return response


def writeItemToFile(item, itemNumber, outputFile, outputWriter):
    itemTitle = str(item['title'])
    itemPrice = float(item['sellingStatus']['convertedCurrentPrice']['value'])
    try:
        outputWriter.writerow({'Number': itemNumber, 'Title': itemTitle, 'Price': itemPrice})
    except:
        print("Item number: " + str(itemNumber) + " failed to print")


def returnAllCurrentResults(itemNumber, outputFile, outputWriter, keyword):
    # TODO check to see if returned results are greater than 10000

    response = getInitialResponse('findItemsAdvanced', keyword)
    returnedItems = getTotalReturnedItems(response)
    totalPages = getTotalNumberOfPages(returnedItems)

    print('Printing ' + str(returnedItems) + ' Currently Listed Items')
    for i in range(totalPages):
        response = makefindAdvancedItemsAPICall(i)
        print('Writing results from page[' + str(i+1) +"/" + str(totalPages) +']')
        for item in response.dict()['searchResult']['item']:
            itemNumber = int(itemNumber+1)
            writeItemToFile(item, itemNumber, outputFile, outputWriter)
    return itemNumber


def returnAllPastResults(itemNumber, outputFile, outputWriter, keyword):
    # TODO check to see if returned results are greater than 10000

    response = getInitialResponse('findCompletedItems', keyword)
    returnedItems = getTotalReturnedItems(response)
    totalPages = getTotalNumberOfPages(returnedItems)
    print('Printing ' + str(returnedItems) + ' Previously Listed Items')
    for i in range(totalPages):
        response = makeFindCompletedItemsAPICall(i)
        print('Writing results from page[' + str(i+1) +"/" + str(totalPages) +']')
        for item in response.dict()['searchResult']['item']:
            itemNumber = int(itemNumber+1)
            writeItemToFile(item, itemNumber, outputFile, outputWriter)
    return itemNumber


def getTotalReturnedItems(response):
    returnedItems = int(response.dict()['paginationOutput']['totalEntries'])
    return returnedItems


def getTotalNumberOfPages(returnedItems):
    totalPages = math.ceil(returnedItems/100)
    return totalPages


def mainFunction(api):
    keyword = input('Enter search keyword: ')
    fileName = input('Enter the name of the file you would like this data written to: ')+'.csv'
    print('')

    with open(fileName, 'w', newline='') as csvfile:
        fieldnames = ['Number', 'Title', 'Price']
        outputWriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
        outputWriter.writeheader()
        itemNumber = returnAllCurrentResults(0, csvfile, outputWriter, keyword)
        itemNumber = returnAllPastResults(itemNumber, csvfile, outputWriter, keyword)
        csvfile.close()

    print('Total Items Printed: ' + str(itemNumber))
    print('Results printed to ' + str(fileName))


api = Finding(appid='TaylorMo-PythonEB-PRD-e5d865283-1005e2c5', config_file=None)
mainFunction(api)
