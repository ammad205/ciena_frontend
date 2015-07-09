#!/usr/bin/env python
import urllib2
import StringIO
from xml.dom.minidom import parse


class xmlparser():


    def __init__(self):
        self.vm_uuid = ''
        self.mgmt_ip_address = ''
        self.vm_name = ''


    def getVm_uuid_mgmtip(self,vm_name):
        self.getandParseResults(vm_name)
        return self.vm_uuid, self.mgmt_ip_address

    def getandParseResults(self,vm_name):
	print "+++++++++++++++++++++++++vm name is : ",vm_name
        vm_name = 'firefly_48'
        response = urllib2.urlopen('http://192.168.7.225:8085/Snh_ItfReq')
        textresponse = response.read()
        dom = parse(StringIO.StringIO(textresponse))


        #itf_resp = dom.documentElement
        #itf_sandesh_data_items=itf_resp.getElementsByTagName('ItfSandeshData')
        #print itf_sandesh_data_items.length

        list_vm_name = dom.getElementsByTagName('vm_name')
        print type(list_vm_name)
        length_list= list_vm_name.length
        print dom.getElementsByTagName('vm_name')[12].childNodes[0].nodeValue




        for i in range(0,len(list_vm_name)-1):


            check_childs_count = dom.getElementsByTagName('vm_name')[i+1].childNodes
            if check_childs_count.length > 0:
                if vm_name == dom.getElementsByTagName('vm_name')[i+1].childNodes[0].nodeValue:
                    print dom.getElementsByTagName('vm_name')[i+1].childNodes[0].nodeValue
                if 'default-domain:admin:svc-vn-mgmt' == dom.getElementsByTagName('vn_name')[i+1].childNodes[0].nodeValue:
                    self.mgmt_ip_address = dom.getElementsByTagName('mdata_ip_addr')[i+1].childNodes[0].nodeValue
                    print self.mgmt_ip_address
                    self.vm_uuid = dom.getElementsByTagName('vm_uuid')[i+1].childNodes[0].nodeValue
                    print self.vm_uuid
                    #print node.getElementsByTagName('vm_name').childNodes[0].nodeValue






