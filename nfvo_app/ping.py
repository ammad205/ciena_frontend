#!/usr/bin/env python
import paramiko
import pexpect
import time
import xmlparser
from novaclient.client import Client

class getPingStatus():

    def __init__(self,vm_name):
	self.vm_name = ''
	self.ping_result = ''
	self.vm_status = ''
	self.vm_uuid = ''
	self.mgmt_ip_address = ''




    def getLatestStatus(self,vm_name):
	print "virtual machine name is :"
	print vm_name
	# xmlparser_obj = xmlparser.xmlparser()
	# self.vm_uuid , self.mgmt_ip_address = xmlparser_obj.getVm_uuid_mgmtip(vm_name)

	self.vm_uuid = self.get_uuid_vm(vm_name)
	try:
		print "going for console connection>>>>>>>>>"
	        console_cmd = 'virsh console ' + self.vm_uuid
                print console_cmd

	except Exception,e:
			       print e
	                       return 'NotActive','NotAvailable' , 'NoStatus'

	session = pexpect.spawn(console_cmd)
	session.expect('.+')
	valid_string = session.after
	print valid_string
	session.send("\r\n")
	session.expect('.+')
	valid_string = session.after
	print valid_string
	print "session closed"
	session.send('root')
	session.expect('.+')
	print session.after
	session.send("\r\n")
	session.expect('.+')
	print session.after
	session.send('c0ntrail123')
	session.expect('.+')
	print session.after
	session.send('\r\n')
	session.expect('.+')
	print session.after
	session.send("touch root.txt")
	session.expect('.+')
	print session.after
	session.send("\r\n")
	session.expect('.+')
	print session.after
	session.sendline("ping 4.2.2.4")
	time.sleep(2)
	session.expect('.+')
	print session.after
	session.send('\x03')
	session.expect('.+')
	self.ping_result = session.after
	print self.ping_result
	session.close(force=True)

	self.comment,self.ping_result = self.make_decision(self.ping_result)

	return self.ping_result, 'Available', self.comment

    def get_uuid_vm(self, vm_name):
        nova = Client(1.1, 'admin', 'Jintac123', 'admin', 'http://192.168.7.225:5000/v2.0')
        srv = nova.servers.find(name=vm_name)
        return srv.id

    def make_decision(self,complete_ping_message):
	print '*************************************'
	print complete_ping_message
	message_splitted = complete_ping_message.strip().split('-\r\n')
	print "++++++++++++++++++++" ,  message_splitted
	print "message splitted is ::::::::::::"
	#len(message_splitted)
	new_split_message = message_splitted[1].split(',')
	print "new split message is ::::::  "
	print new_split_message
	pckts_transmitted = new_split_message[0]
	pckts_received = new_split_message[1]
	pckts_loss = new_split_message[2]
	#time_taken = split_message2[3]
	pckts_transmitted_value = int(pckts_transmitted.strip().split(' ')[0])
	pckts_received_value = int(pckts_received.strip().split(' ')[0])
	pckts_loss_pvalue = int(pckts_loss.strip().split('%')[0].strip())
	if pckts_loss_pvalue > 5 and pckts_loss_pvalue < 10:
	    print "success*******************"
	    return 'good', 'Active'
	elif pckts_loss_pvalue > 10 and pckts_loss_pvalue < 50:
	    return 'fair', 'Active'
	elif pckts_loss_pvalue > 50 and pckts_loss_pvalue < 95:
	    return 'poor', 'Active'
	elif pckts_loss_pvalue > 95:
	    return 'no connectivity', 'NotActive'