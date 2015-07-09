from multiprocessing import Process
from zaqarclient.queues.v1 import client
from modeler_infra import modelertest

class MyProcess(Process):
    URL = 'http://localhost:8888'
    queue_name = 'myqueue'
    queue = ''
    messages = []

    mm =  modelertest.ModelerTest()
    

    def __init__(self):
        Process.__init__(self)
        self.createConnection()

    def createConnection(self):
        cli = client.Client(self.URL)
        self.queue = cli.queue(self.queue_name)

    def run(self):
        with open("pubsubinfra_workerf.txt", "w") as f:	
	    while(True):
	        for msg in self.queue.messages(echo=True):
                    print(msg.body)
		    f.write(str(msg.body)+ "\n")
                    self.mm.main_func(str(msg.body))
    
	    

if __name__ == "__main__":
    p = MyProcess()
    p.start()
    print ("process id is : %s \n" %p.pid)
    p.join()
    print p.exitcode





   



