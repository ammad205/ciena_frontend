__author__ = 'awais'

from time import gmtime, strftime

from novaclient.client import Client
#import Functions
from configs import *
from django.shortcuts import HttpResponse
import time

##Make user and tenant


class FireFly():
    # def __init__(self):
        # nova = Client(1.1, 'admin', 'secret123', 'admin', 'http://192.168.7.10:5000/v2.0')



    def spawn_vm(self, vm_name,  username, password, tenant, nics):


 #       fun = Functions()
        #nova = fun.validate_token(username, password, tenant)
        nova = Client(1.1, 'admin', 'Jintac123', 'admin', 'http://192.168.7.225:5000/v2.0')
        image = nova.images.find(name=firefly_image)
        flavor = nova.flavors.find(name=firefly_flavor)
        print "in spawn function",image,flavor
            # tenant_name = get_tenant_name(self)
        try:

            #instance_name = "firefly"+"_"+strftime("%S", gmtime())
            print "instance name",vm_name
            print "nics list in try ",nics
            res = nova.servers.create(vm_name, image, flavor,nics=nics)

            print res
            st = self.wait_for_spawn(vm_name, 'BUILD', nova)

            print "res id and res.name",res.id, res.name
            print nova 
            print "return values in sapwn vm are",res.id,res.name,nova
            return (res.id, res.name,nova)
        except Exception,e:
            return e

    def delete_vm(self, request):
        vm_name = request.REQUEST["vm_name"]
        nova = Client(1.1, 'admin', 'jintac123', 'admin', 'http://192.168.7.225:5000/v2.0')
        instance_found = False
        try:
            list_of_instances = nova.servers.list()
            for srv in list_of_instances:
                if srv.name == vm_name:
                    print ("Looking for Instance....")
                    instance_found = True
                    break
            if instance_found:
                print ("Found instance %s for deletion" % srv.name)
                nova.servers.delete(srv)
                print ("Deleted the instance %s" % vm_name)
        except Exception, e:
            return HttpResponse(e)
        return HttpResponse("server deleted")

    ## ss = nova.servers.find(vm_name)
    # nova.servers.delete(ss)



    def wait_for_spawn(self, vm_name, status, nova, timeout=None):
        if timeout is None:
            timeout = 10
        print "in wait for spawn "
        #nova = self.validate_token()
        while timeout:
            print "sleep for 15 seconds"
            time.sleep(15)
            vm = nova.servers.find(name = vm_name)
            print vm_name
            print vm
            # get configs from server

            # vm = self.conn.servers.find(name = vm_name)
            if vm.status != status:
                print 'VM %s is in state %s' %(vm.name, vm.status)
                break
            timeout -= 1
        return True

