import json
from error_manager import Error_Handler

import sqlite3
from error_manager import Error_Handler
# with open(file = 'kz-mac-4.json',
#           mode = 'w',
#           encoding= 'UTF-8') as fw:
#     data = json.loads(fw)
#     print(data)
# for plan in data:
#     for t in plan['tasks']:
#         monitor = t['monitorType'].split(',')
from db_manager import LocalDB

with open(file = 'kz-mac-4.json',
          mode = 'w',
          encoding='UTF-8') as f:
    fileData = []
    for line in f:
        fileData.append(line)
    print(fileData)

db = LocalDB('db/task.db')
for data in fileData:
    data = json.load(json.load(data))
    print(data)
