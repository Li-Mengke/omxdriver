import sqlite3
from db_manager import LocalDB
import json

with open('kz-mac-4.json',encoding='utf-8') as f:
#     fileData = []
#     for line in f:
#         fileData.append(line)
#     print(fileData)
# db = LocalDB('db/task.db')
#for data in fileData:
    #print(data)
#filedata是一个list,内容的类型是字典
    filedata = json.load(f)
    plist = []
    dlist = []
#print(filedata)
#将filedata的每项解析为q（字典）并做处理
for i in range(len(filedata)):
    #print(filedata[i],'\n')
    q = filedata[i]
    if q['messageType'] == 'putinto-task':
        content = q['content']  #putinto-task的内容是一个列表
        for l in range(len(content)):  #解析content
            if 'materialName' in content[l]:
                #lcon 是上刊名列表
                plist.append(content[l]['materialName'])
        #put_into_task()
        #********'这里加上日志'
    #else:
    elif q['messageType'] =='down-task':
        for l in range(len(content)):  #解析content
            if 'materialName' in content[l]:
                #dlist 是上刊名列表
                dlist.append(content[l]['materialName'])
