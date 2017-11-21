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
