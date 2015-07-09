#!/usr/bin/env python
import paramiko
import pexpect
import os
import glob
import sys
import time
from commands import *
import xml.etree.ElementTree as ET
from novaclient.client import Client



"""
Vsrx
Supposition:We have firefly image in our openstack DB,from it we create the new nfv and we know its username and password.


Argument Name: nfv_uuid 
Description: UUID of the spawning nfv for commands injection 

Argument Name: nfv_name
Description: Name of the nfv for spawnnig

Argument Name:commands
Description:Set of commands that needs to be executed

Argument Name:Medium
Description: Medium either the transport layer used ssh or serial

Argumnet Name:Username
Description: Internal username of the vSRX image in which we insert commmands

Argument Name: Password
Description: Internal password of the virtual machine
  
"""
class Vsrx():
    def __init__(self, uuid,medium,username,password,commands,name,nova):
        self.uuid = uuid
        self.medium = medium
        self.username = username
        self.password = password
        self.name = name
        self.commands = commands
        self.nova = nova
    def service_netconf_enable(self):
        print 'Enable NETCONF service using SSH .'
  	ssh = paramiko.SSHClient()
  	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  	ssh.connect(self.mgmt_addr, username = 'root', password = 'passWD')
        "FUNCTION HAVING MULTIPLE COMMANDS"
  	ssh.exec_command('cli -c "configure;set system services netconf ssh;set security zones security-zone trust interfaces ge-0/0/0.0 host-inbound-traffic system-services all;commit"')
  	time.sleep(10)
  	ssh.close()


    def command(self):
        list = []
        #print "List of commands"
        cmd1 = 'cli -c "configure;set system services netconf ssh;set security zones security-zone trust interfaces ge-0/0/0.0 host-inbound-traffic system-services all;commit"'
        return cmd1       

        

    def serial_console_insertion(self,console_cmd):
        print "Check validity for serial console "
  	validation_list = ['Active console session exists for this domain','internal error character device (null) is not using a PTY','login:']
        print "session initiation"
        session = pexpect.spawn(console_cmd)
  	session.expect('.+')
	valid_string = session.after
        print valid_string
        session.send("\r\n")
        #session.send("\r\n")
        session.expect('.+')
        valid_string = session.after
        print valid_string
        #cmd = self.commands()
        cmd = self.command()
        if validation_list[0] in valid_string or validation_list[1] in valid_string:
            print "Not connected to serial console"
    	    print validation_list[0]
    	    session.kill(0)
        elif validation_list[2] in valid_string:
            #print "prompt for root and password"
            #print validation_list[2]
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
            session.sendline(cmd)
            session.expect('.+')
            print session.after
            #print "sleeping root password"
            time.sleep(10)
        else:
            print "sending commands"
            session.send("touch nahi.txt")
            session.send("\r\n")
            session.send(cmd)
            print "sleeping"
            time.sleep(10)
        print "Session closed"
        session.close(force=True)
        print session.isalive()

        
    def get_vm_name(self):
        print "Mapping of virtual machine name from openstack to libvirt"
        vm_name = "virsh dominfo %s | sed '2!d' | awk '{print$2}'" % (self.uuid)
        print vm_name
        nfv_name = getoutput(vm_name)
        print nfv_name
        return nfv_name

    def serial_console_conn(self):
        print "sleeping f0r 60 seconds"
        time.sleep(60)
        print "serial console connection command"
  	console_cmd = 'virsh console %s' % (self.uuid)
        print console_cmd
        return console_cmd



    def serial_console_enable(self):
        print "serial console support adding on host side"
        libvirt_xml = '%s.xml'%(self.uuid)
        virsh_command_first = "virsh dumpxml --inactive --security-info %s > /tmp/%s" %(self.uuid,libvirt_xml)
        print virsh_command_first
        self.commands_execute(virsh_command_first)
        self.xml_modification(libvirt_xml)
        virsh_command_second = "virsh define /tmp/%s"%(libvirt_xml)
        print virsh_command_second
        self.commands_execute(virsh_command_second)
        virsh_command_third = "virsh destory %s" % (self.uuid)
        print virsh_command_third
        self.commands_execute(virsh_command_third)
        nova_obj = self.nova_soft_reboot()
        #libvirt_del = "rm -f /tmp/%s" % (libvirt_xml)
        #self.commands_execute(libvirt_del)
        print "sleep for 90 sec"
        self.sleep(90)
        return nova_obj


    def nova_soft_reboot(self):
        print "soft reboot the virtual machine after updating the xml file"
        from novaclient.client import Client
        nova_obj = Client(1.1, 'admin', 'Jintac123', 'admin', 'http://192.168.7.225:5000/v2.0')
        print "rebooting virtual machine"
        vm = nova_obj.servers.reboot(self.uuid)
        return nova_obj


    def xml_modification(self,libvirt_xml):
        print "Adding serial console tags"
        print libvirt_xml
        targets = '/tmp/%s' %(libvirt_xml)
        print targets
        print targets
        tree = ET.parse(targets)
        root = tree.getroot()
        for dev in root.getiterator('devices'):
            for serial in dev.getiterator("serial"):
                dev.remove(serial)
            for console in dev.getiterator("console"):
                dev.remove(console)
        for devices in root.getiterator("devices"):
            serial_node = "serial"
            serial_subnode = "target port='0'"
    	    serial = ET.Element(serial_node)
            serial.set('type','pty')
            serialsubnode = ET.SubElement(serial,serial_subnode)
            console_node = "console"
            console_subnode = "target type='serial' port='0'"
            console = ET.Element(console_node)
            console.set('type','pty')
            consolesubbnode = ET.SubElement(console,console_subnode)
            devices.append(serial)
            devices.append(console)
        print ("channel and serial tag added")
        tree.write(targets)
       
    

    def commands_execute(self,command):
        print "commands for execution"
        print command
        execute = getoutput(command)
        

    def check_status_vm(self,nova):    
        print "wait for virtual machine reboots completely"         
        timeout = 14
	while timeout:
            print "sleep for 15 seconds"
            time.sleep(15)
            print  self.name
            vm = nova.servers.find(name = self.name)
            if vm.status != 'REBOOT':
                print 'VM %s is %s' %(vm.name, vm.status)
                #time.sleep(30)
                break
            timeout -= 1

    def sleep(self,seconds):
        time.sleep(seconds)


    def communication_medium(self):
        if self.medium == 'ssh':
            self.service_netconf_enable(self)    
        else:
            self.serial_console_insertions(self)
  
    def main(self):
    	print "nfv name"
    	nfv_name = self.get_vm_name()
    	print nfv_name
    	print "serial consle enable"
    	nova_obj = self.serial_console_enable()
    	print "check status"
    	second = self.check_status_vm(nova_obj)
    	print "connect console"
    	time.sleep(60)
    	console_cmd = self.serial_console_conn()
    	print "inject command"
    	third = self.serial_console_insertion(console_cmd)
    	#else:
                  
if __name__ == '__main__':
    nfv = Vsrx(uuid="de548845-ab29-48ad-b0a0-f6312f426322",medium="serial",username="root",password='c0ntrail123',name='FF_testing_ssh')
    #if medium == "serial":
    print "nfv name"
    nfv_name = nfv.get_vm_name()
    print nfv_name
    print "serial consle enable"
    nova = nfv.serial_console_enable()
    print "check status"
    second = nfv.check_status_vm(nfv_name,nova)
    print "connect console"
    time.sleep(60)
    console_cmd = nfv.serial_console_conn()
    print "inject command"
    third = nfv.serial_console_insertion(console_cmd)
    #else:
    #    ssh = nfv.service_netconf_enable(self)
        


