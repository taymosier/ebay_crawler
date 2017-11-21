import pprint
import math
import csv
import time
from ebaysdk.finding import Connection as Finding
from ebaysdk.exception import ConnectionError

def makeAPICall(i):
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

def writeItemToFile(item, itemNumber, outputFile, outputWriter):
    itemTitle = str(item['title'])
    itemPrice = float(item['sellingStatus']['convertedCurrentPrice']['value'])
    try:
        outputWriter.writerow({'Number': itemNumber, 'Title': itemTitle, 'Price': itemPrice})
    except:
        print("Item number: " + str(itemNumber) + " failed to print")

def returnAllResults(itemNumber, outputFile, outputWriter, totalPages):
    # TODO check to see if returned results are greater than 10000
    for i in range(totalPages):
        response = makeAPICall(i)
        print('Writing results from page[' + str(i+1) +"/" + str(totalPages) +']')
        for item in response.dict()['searchResult']['item']:
            itemNumber = int(itemNumber+1)
            writeItemToFile(item, itemNumber, outputFile, outputWriter)
    return itemNumber

def mainFunction(api):
    print('')
    keyword = input('Enter search keyword: ')
    fileName = input('Enter the name of the file you would like this data written to: ')+'.csv'
    response = api.execute('findItemsAdvanced', {'keywords': str(keyword)})
    returnedItems = int(response.dict()['paginationOutput']['totalEntries'])

    totalPages = math.ceil(returnedItems/100)

    with open(fileName, 'w', newline='') as csvfile:
        fieldnames = ['Number', 'Title', 'Price']
        outputWriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
        outputWriter.writeheader()
        itemNumber = returnAllResults(0, csvfile, outputWriter, totalPages)
        csvfile.close()

    print('Initial total returned results: ' + str(returnedItems))
    print('Total Items Printed: ' + str(itemNumber))
    print('Results printed to ' + str(fileName))

api = Finding(appid='TaylorMo-PythonEB-PRD-e5d865283-1005e2c5', config_file=None)
mainFunction(api)
