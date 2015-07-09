#!usr/bin/env python
#from ngn_grid.apps.modeler_infra.functions import Functions
from novaclient.client import Client

class Network():
    def network_list(self):
        print "in network list"
        #fun = Functions()
        #nova = fun.validate_token(username,password,tenant)
        nova = Client(1.1, 'admin', 'Jintac123', 'admin', 'http://192.168.7.225:5000/v2.0')
        network_list = []
        network_list_obj = nova.networks.list
        for n in range(len(network_list_obj())):
            print network_list_obj()[n].label
            network_list.append(network_list_obj()[n].label)
        return network_list



    def networks(self,mngt_ntwrk,left_ntwrk,rigt_ntwrk):
        print "networks"
        nova = Client(1.1, 'admin', 'Jintac123', 'admin', 'http://192.168.7.225:5000/v2.0')
        nics = []
        network_list_obj = nova.networks.list
        for n in range(len(network_list_obj())):
            if mngt_ntwrk in network_list_obj()[n].label:
                nics.append({"net-id":network_list_obj()[n].id})
            if left_ntwrk in network_list_obj()[n].label:
                nics.append({"net-id":network_list_obj()[n].id})
            if rigt_ntwrk in network_list_obj()[n].label:
                nics.append({"net-id":network_list_obj()[n].id})
        print "THIS IS NIC",nics
        return nics
        
    def fast_network_list(self):
        print "fast network list"
        nova = Client(1.1, 'admin', 'Jintac123', 'admin', 'http://192.168.7.10:5000/v2.0')
        network_lst = []
        network_list = nova.networks.list()
        for n in range(len(network_list)):
            #print network_list[n].label
            network_lst.append(network_list[n].label)
        print "THIS IS NWTORK LIST",network_list
        #j={}    
        return network_lst 
