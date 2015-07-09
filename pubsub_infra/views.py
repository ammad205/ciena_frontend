from django.shortcuts import render
import modeler_infra
# Create your views
from zaqarclient.queues.v1 import client
URL = 'http://localhost:8888'
queue_name = 'myqueue'
queue = ''
messages = []

def postMessage(self,message):
    print "123"
    cli = client.Client(URL)
    print "456"
    queue = cli.queue(queue_name)
    print "678"
    queue.post(messages)
    print "999999"


def createConnection(self):
     cli = client.Client(URL)
     queue = cli.queue(queue_name)


def spawnModeler(self):
     for msg in queue.messages(echo=True):
     print(msg.body)
     main_func(msg.body)

