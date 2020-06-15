import sqlite3
from db_manager import LocalDB
import json

with open('kz-mac-4.json',encoding='utf-8') as f:
    fileData = []
    for line in f:
        fileData.append(line)
    print(fileData)
db = LocalDB('db/task.db')
for data in fileData:
    #print(data)
    data = json.loads(json.load(data))