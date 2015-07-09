#!/usr/bin/env python
import paramiko
import pexpect
import time




def pingIpAddresses(self):
    console_cmd = "virsh console instance-00000009"
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
    session.sendline("ping 8.8.8.8")
    time.sleep(10)
    session.expect('.+')
    print session.after
    session.send('\x03')
    session.expect('.+')
    self.pingoutput = session.after
    print self.pingoutput
    session.close(force=True)





def printResults(self):
    splittedmessage = self.pingoutput.split(',')
    print splittedmessage



def main():
    print "Hello, world!"
    pingIpAddresses()
    printResults()
    time.sleep(50)


if __name__ == '__main__':
    main()
