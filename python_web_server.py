#!/usr/bin/env python3



from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from queue import Queue
import json, os, multiprocessing

from server.errors import ConfigError



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
    global port, thread_limit

    config = loadConfig(path)

    if 'root' in config:
        os.chdir(config['root'])
    else:
        raise ConfigError(
            config_file=path,
            message='No root property',
        )

    if 'port' in config:
        port = config['port']
    else:
        port = 80

    if 'threads per core' in config:
        threads_per_core = config['threads per core']
    else:
        threads_per_core = 4

    if 'thread limit' in config:
        thread_limit = config['thread limit']
    else:
        thread_limit = multiprocessing.cpu_count() * threads_per_core

def respond(requests):
    '''
    Get HTTP message from socket in requests queue.
    Send response, close connection, repeat.
    '''

    connectionSocket, clientAddress = requests.get()
    message = connectionSocket.recv(2048).decode('utf-8')
    # parse http message
    # load requested object
    # generate response
    # send response
    connectionSocket.close()


# execute necessary setup routines
setConfig('web.json')
requests = Queue()
for i in range(thread_limit):
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
