import sys
import commands
import json
import os


username = sys.argv[1]
email = sys.argv[2]
API_Key = sys.argv[3]
API_KEY_SECRET = sys.argv[4] 
cmd1 = "git config --global user.name '%s'"%(username)
print cmd1
cmd2 = "git config --global user.email '%s'"%(email)
print cmd2
cmd3 = 'ssh-keygen -b 2048 -t rsa -f ~/.ssh/id_rsa -q -N "" -C "%s"'%(email)
print cmd3
cmd_lst = [cmd1,cmd2,cmd3]
for cmd in cmd_lst: 
  print cmd
  status = commands.getoutput(cmd)
  print status

cmd4 = "cat ~/.ssh/id_rsa.pub"
status = commands.getoutput(cmd4)
json_strs = '{"key":"%s", "title":"%s"}'%(status,username)
print json_strs
#cmd5 = """curl -i -X POST -H "X-Api-key: 2b914f51ba6fecfb83cd" -H "X-Api-secret: 151e88cc4cbcc9f8f012fbdb389afb36a6f6ee5d" -H "Content-type: application/json" -d '%s' --insecure https://api.assembla.com/v1/user/ssh_keys.json """%(json_strs)
cmd5 = """curl -i -X POST -H "X-Api-key: %s" -H "X-Api-secret: %s" -H "Content-type: application/json" -d '%s' --insecure https://api.assembla.com/v1/user/ssh_keys.json """%(API_Key,API_KEY_SECRET,json_strs)
status = commands.getoutput(cmd5)
print status

cmd6 = "git clone git@git.assembla.com:nfvo.git"
print cmd6
status = commands.getoutput(cmd6)





