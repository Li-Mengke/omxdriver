import pika
import yaml
import requests
import json
import os

'''this part gets the message from rabbitmq'''
with open('application-dev.yml') as f:
    var = yaml.load(f, Loader = yaml.SafeLoader)

host_name = var['rabbitmq']['host']
port = var['rabbitmq']['port']
user_name = var['rabbitmq']['username']
password = var['rabbitmq']['password']

MAC_Address = 'mac-123456'
queue_name = MAC_Address + '_queue'
exchangeName = "qutou.osp-exchange"
queue_name = MAC_Address + '-queue'
routing_key = MAC_Address + '-routingKey'

def callback(ch, method, properties, body):
    with open("mqresult.txt", 'a') as f:
        f.write(body.decode("utf-8"))
    print(body)

credentials = pika.PlainCredentials(user_name, password)
parameters = pika.ConnectionParameters(host = host_name, port = port, virtual_host='/', credentials = credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.basic_consume(queue = queue_name, on_message_callback = callback, auto_ack= True)



channel.start_consuming()



with open('mqresult.txt') as f:
    data = json.load(f)

url = data['content']['putintoTask']['url']
fileName = data['content']['putintoTask']['materialName']



def download(url, fileName):
    if os.path.exists(fileName):
        header = requests.head(url)
        fileLength = int(header.headers['Content-Length'])
        if fileLength == os.path.getsize(fileName):
            return True
        else:
            with open(fileName, 'ab') as f:
                position = f.tell()-1024
                pos_header = {}
                print(position)
                pos_header['Range'] = f'bytes={position}-'

            with requests.get(url, headers = pos_header, stream = True) as r:
                with open(fileName, 'ab') as f:
                        #some validation should be here

                    for chunk in r.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(r.content)
                            f.flush()
                            print(os.path.getsize(fileName))

    else:
        with requests.get(url, allow_redirects=True, stream = True) as r:
            with open(fileName, 'wb') as f:
                iter = 0
                for chunk in r.iter_content(chunk_size = 1024):
                    if chunk:
                        f.write(chunk)
                        f.flush()
                        iter += 1
                    if iter > 2000:
                        break

result = download(url, fileName)
print(result)