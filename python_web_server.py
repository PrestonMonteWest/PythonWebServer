#!/usr/bin/env python3



from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from queue import Queue
import json, os, multiprocessing

from server.errors import ConfigError
from server.http import HttpResponse



def loadConfig(path):
    '''
    Load JSON config file from <path>.
    Return the resulting dict.
    '''

    with open(path) as f:
        config = json.loads(f.read())

    return config

def setConfig(path):
    '''
    Set server config variables using config file <path>.
    Defaults should be assumed when appropriate (e.g., port 80 for web serving).
    '''

    # config variables
    global port, threadLimit

    config = loadConfig(path)

    if 'root' in config:
        os.chdir(config['root'])
    else:
        raise ConfigError(
            configFile=path,
            message='No root property',
        )

    if 'port' in config:
        port = config['port']
    else:
        port = 80

    if 'threads per core' in config:
        threadsPerCore = config['threads per core']
    else:
        threadsPerCore = 4

    if 'thread limit' in config:
        threadLimit = config['thread limit']
    else:
        threadLimit = multiprocessing.cpu_count() * threadsPerCore

def respond(requests):
    '''
    Get HTTP message from socket in requests queue.
    Send response, close connection, repeat.
    '''

    connectionSocket, clientAddress = requests.get()
    message = connectionSocket.recv(4096).decode('utf-8')
    connectionSocket.send(str(HttpResponse(message)).encode('utf-8'))
    connectionSocket.close()



# execute necessary setup routines
setConfig('web.json')
requests = Queue()
for i in range(threadLimit):
    Thread(target=respond, args=(requests,)).start()

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', port))
serverSocket.listen(1)
print('Web server is listening on 127.0.0.1:{0}...'.format(port))

try:
    while True:
        connectionSocket, clientAddress = serverSocket.accept()
        print('{0} created for {1}'.format(connectionSocket, clientAddress))
        requests.put((connectionSocket, clientAddress))
finally:
    serverSocket.close()
