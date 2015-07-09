import platform
import commands


def chk_linux_flavor():
  flavor = platform.linux_distribution()
  print flavor
  return flavor

def chk_python_version():
  ver = platform.python_version()
  print ver
  return ver

def chk_pkg(pkg_list):
  for pkg_name in pkg_list:
    cmd = "%s --version" % (pkg_name)
    status = commands.getoutput(cmd)
    print status
  return status

def chk_pkg(pkg_list):
  dic_status = {}
  for pkg_name in pkg_list:
    cmd = "%s --version" % (pkg_name)
    status = commands.getoutput(cmd)
    dic_status[pkg_name] = status
    #print dic_status     
    print status
  return dic_status

def install_pkg(instll_cmd,pkg_name):
  cmd = "%s install %s" % (instll_cmd,pkg_name)
  status = commands.getoutput(cmd)
  print status
  return status


def mkvirtual_env(): 
  cmd_list = ["mkdir /home/NFV","virtualenv /home/NFV/NFVO"," source /home/NFV/NFVO/bin/activate"]
  for cmd in cmd_list:
    print cmd
    status = commands.getoutput(cmd)
  print status
  return status

def main_func():
  flavor = chk_linux_flavor()
  version = chk_python_version()
  pkg_list = ['pip','virtualenv']
  dic_status = chk_pkg(pkg_list)
  for key,value in dic_status.items():
    if "not" in dic_status[key]:
      if 'CentOS' in flavor[0]:
        if dic_status[key] == "pip":
          install_cmd = "yum"
          print install_cmd
        else:
          install_cmd = "pip"
          print install_cmd
        pkg_name = dic_status[value]
        install_pkg(install_cmd,pkg_name) 
      else:
        if dic_status[key] == "pip":
          install_cmd = "apt-get"
        else:
          install_cmd = "pip"
        pkg_name = dic_status[value]
        install_pkg(install_cmd,pkg_name) 
    else:
      print "aws"
      status = mkvirtual_env()
      
         

if __name__ == "__main__":
  print "hello"
  main_func()
  print "hi"

