import pprint
import math
import csv
import time
from ebaysdk.finding import Connection as Finding
from ebaysdk.exception import ConnectionError

api = Finding(appid='TaylorMo-PythonEB-PRD-e5d865283-1005e2c5', config_file=None)

response = api.execute('findCompletedItems', {
'keywords': 'Cracker Barrel',
'paginationInput': {
'entriesPerPage': '100',
'pageNumber': '1'
}
})

pprint.pprint(response.dict())

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

def returnAllCurrentResults(itemNumber, outputFile, outputWriter, keyword):
    # TODO check to see if returned results are greater than 10000

    response = getInitialResponse('findItemsAdvanced', keyword)
    returnedItems = getTotalReturnedItems(response)
    totalPages = getTotalNumberOfPages(returnedItems)

    print('Printing ' + str(returnedItems) + ' Currently Listed Items')
    for i in range(totalPages):
        time.sleep(.05)
        # response = makefindAdvancedItemsAPICall(i)
        response = makeAPICall(i, 'findItemsAdvanced')
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
    print('')
    print('Printing ' + str(returnedItems) + ' Previously Listed Items')
    for i in range(totalPages):
        time.sleep(.05)
        # response = makeFindCompletedItemsAPICall(i)
        response = makeAPICall(i, 'findCompletedItems')
        print('Writing results from page[' + str(i+1) +"/" + str(totalPages) +']')
        for item in response.dict()['searchResult']['item']:
            itemNumber = int(itemNumber+1)
            writeItemToFile(item, itemNumber, outputFile, outputWriter)
    return itemNumber
