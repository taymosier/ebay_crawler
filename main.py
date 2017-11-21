import pprint
from ebaysdk.finding import Connection as Finding
from ebaysdk.exception import ConnectionError
try:
    api = Finding(appid='TaylorMo-PythonEB-PRD-e5d865283-1005e2c5', config_file=None)

    response = api.execute('findItemsAdvanced', {'keywords': 'Cracker Barrel'})
    pprint.pprint(response.dict()['paginationOutput']['totalEntries'])
    returnedItems = (response.dict()['paginationOutput']['totalEntries'])





except ConnectionError as e:
    print(e)
    print(e.response.dict())
