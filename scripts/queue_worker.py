from multiprocessing import Process
from zaqarclient.queues.v1 import client
from modeler_infra import modelertest


def run():
    URL = 'http://localhost:8888'
    queue_name = 'myqueue'
    queue = ''
    messages = []
    cli = client.Client(URL)
    queue = cli.queue(queue_name)
    with open("myqueuedata.txt", "w") as f:
        while(True):
            for msg in queue.messages(echo=True):
                print(msg.body)
                f.write(str(msg.body)+ "\n")
                mm.main_func(str(msg.body))
		self.spawnModeler(str(msg.body))
		msg.delete()


def spawnModeler(self,str):
    json_str = str
    #json_str = '{"username":"araza","password":"jin","tenant":"nighter","commands":["netconf","ssh"],"nics":[{"mngt_ntwrk":"svc-vn-mgmt","left$

    import modeler_infra.modeler
    from modeler_infra.modeler import Modeler

    print "***********************************working*****************************99";
    main_obj = modeler_infra.modeler.Modeler();
    data = main_obj.main_func(json_str);
    print data
    print "***********************************working*****************************88";


    return data




def spawn_vm(self, username, password, tenant,nics):
    print "in sapwning"
    fun = Functions()
    #nova = fun.validate_token(username, password, tenant)
    nova = Client(1.1, 'admin', 'secret123', 'admin', 'localhost:5000/v2.0')
    image = nova.images.find(name=firefly_image)
    flavor = nova.flavors.find(name=firefly_flavor)
    # tenant_name = get_tenant_name(self)
    try:
       	##naming scheme
        print "in sapwning 2"
        instance_name = "firefly"+"_"+strftime("%S", gmtime())
        print instance_name
        res = nova.servers.create(instance_name, image, flavor,nics=nics)
        print res
        v = fun.wait_for_spawn(instance_name, 'BUILD', nova)
        print res.id, res.name
        return (res.id, res.name,nova)
    except Exception,e:
        return e

