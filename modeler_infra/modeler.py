#!/usr/bin/env python
import json
import time

#from ngn_grid.apps.modeler_infra import functions
import pyTransportLib
import pyOrchestrateLib
import pyNetworkLib


class Modeler():
	def json_to_obj(self,s):
	    def h2o(x):
	       	if isinstance(x, dict):
		    return type('jo', (),x)
		else:
		    return x
	    return h2o(json.loads(s))

        def transport(self,uuid,medium,username,password,commands,name,nova):
            print uuid,medium,username,password,name,nova
            pytransport = pyTransportLib.Vsrx(uuid,medium,username,password,commands,name,nova)
            pytransport.main()

	def make_tenant_user(self,username,password,tenant):
            obj = functions.Functions()
	    obj.check_for_tenant(username,password,tenant)
            #return status
   

        def orchestrate(self,vm_name,username,password,tenant,nics):
            obj = pyOrchestrateLib.FireFly()
            print "in orchestration function modelr"
            print username,password,tenant,nics
            uuid,name,nova = obj.spawn_vm(vm_name,username,password,tenant,nics)

            #uuid,name = obj.spawn_vm()
            #print uuid
            #print "end"
            return (uuid,name,nova)

        def validation(self,main_obj,param_require):
            print param_require
            #param_require = param_require
	    for l in param_require:
	        boolean = hasattr(main_obj,l)
	        if boolean == True:
	            print "Json object contains parameter %s"%(l)
                else:
                    print "Json has not required parameter %s"%(l)
                    break

        def commands(self,main_obj):
            commands = []
            print "commands"
            if 'netconf' in main_obj.commands:

                cmd1 =  'cli -c "configure;set system services netconf ssh;set security zones security-zone trust interfaces ge-0/0/0.0 host-inbound-traffic system-services all;commit'

                commands += cmd1
            if 'ssh' in main_obj.commands:
                cmd2 =  'cli -c"configure;set system host-name raza;commit"'
                commands += cmd2
            return commands
        def main_func(self,json_str):

            param_require = ['vm_name','username','password','tenant','commands']

    	    #mapper = Modeler()
            print json_str
            print type(json_str)
            print "hello"
            print "Convert json into python object"
            main_obj = self.json_to_obj(json_str)
            print "Validation check compare to required parameters"
            validity = self.validation(main_obj,param_require)
           # print "Make a tenant"

           # self.make_tenant_user(main_obj.vm_name,main_obj.username,main_obj.password,main_obj.tenant)
            print "networking"
            nics = self.assign_nics(main_obj.nics[0]['mngt_ntwrk'],main_obj.nics[0]['left_ntwrk'],main_obj.nics[0]['right_ntwrk'])
            print "orchestration starts"
            uuid,name,nova = self.orchestrate(main_obj.vm_name,main_obj.username,main_obj.password,main_obj.tenant,nics)

  
            print "transport layer"
            time.sleep(80)
            commands = self.commands(main_obj)
            print commands
            self.transport(uuid,'serial','root','c0ntrail123',commands,name,nova)
          
        def network_list(self):
            print "network list return"
            ntwrk_obj = pyNetworkLib.Network()
            fast_net_lst = ntwrk_obj.fast_network_list()
            fast_net_lst = json.dumps(fast_net_lst)
            return fast_net_lst
            
        def assign_nics(self,mngt_ntwrk,left_ntwrk,right_ntwrk):
            ntwrk_obj = pyNetworkLib.Network()
            nics = ntwrk_obj.networks(mngt_ntwrk,left_ntwrk,right_ntwrk)
            print nics
            return nics

if __name__ == '__main__':
    #json_str = {'name':'firefly','uuid':'0d3bf43e-4a1e-44d8-b1ff-425c17e056a8','username':'root','password':'c0ntrail123'}
    json_str = '{"username":"admin","password":"Jintac123","tenant":"admin","commands":["netconf","ssh"],"nics":[{"mngt_ntwrk":"svc-vn-mgmt","left_ntwrk":"DMZ","right_ntwrk":"kq-be"}]}'
    param_require = ['username','password','tenant','commands'] 
    mapper = Modeler()
    mapper.main_func(json_str)
    """
    print "Convert json into python object"
    main_obj = mapper.json_to_obj(json_str)
    
    print "Validation check compare to required parameters"
    validity = mapper.validation(main_obj,param_require)
    print "Make a tenant"
    mapper.make_tenant_user(main_obj.username,main_obj.password,main_obj.tenant)
    print "orchestration starts"
    uuid,name,nova = mapper.orchestrate(main_obj.username,main_obj.password,main_obj.tenant)
    print "transport layer"
    time.sleep(80)
    commands = mapper.commands(main_obj)
    print commands
    mapper.transport(uuid,'serial','root','c0ntrail123',commands,name,nova)
    """



