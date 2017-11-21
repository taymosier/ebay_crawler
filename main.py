import pprint
import math
from ebaysdk.finding import Connection as Finding
from ebaysdk.exception import ConnectionError

# initializes a variable named itemNumber that will be incremented by one
# for each item returned
itemNumber = 0

# defines a function which returns all the results of the query
# it takes the itemNumber variable as a parameter
# https://www.tutorialspoint.com/python/python_functions.htm
# the function is only defined here, it is called (or implemented in the program)
# on line [TODO 'insert line number here']
def returnAllResults(itemNumber):

    # The for statement loops through the code it contains.
    # Consider i to be equal to 0, and i increases by one with each loop.
    # Think of range(totalPages) to be a number range from [0, X],
    # with X being equal to the totalPages variable, which is defined
    # farther down in the program.
    # The loop will repeat until i = X.
    for i in range(totalPages):
        try:
            # the page number of the response variable is updated at the beginning of each loop
            response = api.execute('findItemsAdvanced', {
            'keywords': 'Cracker Barrel',
            'paginationInput': {
            'entriesPerPage': 100,

            # this sets the current page of results to be returned
            # we start with i+1 because i initially equals 0.
            # We must also convert it from a number (or int) to a string (str) variable
            'pageNumber': str(i+1)
            }
            })
            # this tells you the current page that is being printed
            print('Printing page: ' + str(i+1))

            # this is another for loop contained within the other for loop
            # it loops through each returned item result on the current page
            for item in response.dict()['searchResult']['item']:
                # we increase the itemNumber variable by 1 each time a search result item is returned
                itemNumber = itemNumber+1
                # we then print the itemNumber and the title of the item
                print ('Item #: ' + str(itemNumber) + ' - ' + item['title'])
                print('')

        # if the connection times out, it will print an error
        except ConnectionError as e:
            print(e)
            print(e.response.dict())
    return itemNumber

try:
    api = Finding(appid='TaylorMo-PythonEB-PRD-e5d865283-1005e2c5', config_file=None)

    # Specifies search criteria
    print('Enter search keyword')
    keyword = input()

    # Makes initial HTTP request, which means the program sends a request for
    # the requested information to the ebay server. The details of the request
    # are hidden by the api but you don't really need to worry about that at
    # this point. The response variable is set equal to the information that is
    # returned from the ebay server
    response = api.execute('findItemsAdvanced', {'keywords': str(keyword)})

    # Sets returnedItems variable to total number of returned entries.
    # Since the total number of entries are returned as a string, it must
    # be converted to an int
    returnedItems = int(response.dict()['paginationOutput']['totalEntries'])

    # Since the Ebay API only returns a maximum of 100 entries per page,
    # we set the total number of pages to iterate through equal to the
    # total number of returned results divided by 100 and round up
    # using the math.ceil() function
    totalPages = math.ceil(returnedItems/100)

    # prints out the total returned results as a string
    print('Total returned results: ' + str(returnedItems))

    # prints out the total number of pages that will be iterated through
    print('Total pages: ' + str(totalPages))

    # This is the line of code that calls the function we defined at the beginning of the program
    itemNumber = returnAllResults(itemNumber)

    # this prints the original number of items returned and the total number of items printed
    # in order to make sure that all the items we indeed printed
    print('Initial total returned results: ' + str(returnedItems))
    print('Total Items Printed: ' + str(itemNumber))





except ConnectionError as e:
    print(e)
    print(e.response.dict())
