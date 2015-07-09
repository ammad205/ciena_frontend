import platform
import commands
import argparse
import os
def chk_linux_flavor():
    flavor = platform.linux_distribution()
    print "Linux Flavor",flavor
    return flavor


def chk_python_version():
    ver = platform.python_version()
    print "Python Version",ver
    return ver


def chk_pkg(pkg_list):
    status=''
    for pkg_name in pkg_list:
        cmd = "%s --version" % (pkg_name)
        status = commands.getoutput(cmd)
        print status
    return status


def chk_pkg(pkg_list, flavor):
    dic_status = {}
    for pkg_name in pkg_list:
        cmd = "%s --version" % (pkg_name)
        status = commands.getoutput(cmd)
        if "python2.6" in status:
            print "pip installed but with python2.6"
            if 'CentOS' in flavor[0]:
                install_cmd = [
                    "wget https://raw.githubusercontent.com/pypa/pip/master/contrib/get-pip.py --no-check-certificate",
                    "python2.7 /home/get-pip.py", "pip2.7 install virtualenv"]
                for cmd in install_cmd:
                    status = commands.getoutput(cmd)
                    print cmd
                print status
        dic_status[pkg_name] = status
        cmd = "pip2.7 install virtualenv"
        print "Virtual ENV", cmd
        statuse = commands.getoutput(cmd)
        print statuse
        print status
    return dic_status


def install_pkg(install_cmd, pkg_name):
    cmd = "%s install %s" % (instll_cmd, pkg_name)
    status = commands.getoutput(cmd)
    print status
    return status


def mkvirtual_env(directory_path,directory_name,virtual_env_name):
   
    cmd_list = ["mkdir /home/jintac","virtualenv /home/jintac/jintac-nfvo",
                " source /home/jintac/jintac-nfvo/bin/activate",
                "/home/jintac/jintac-nfvo/bin/pip2.7 install Django==1.7.1", "/home/jintac/jintac-nfvo/bin/pip2.7 install mysql-python",
				"/home/jintac/jintac-nfvo/bin/pip2.7 install pexpect", "/home/jintac/jintac-nfvo/bin/pip2.7 install django-extensions",
				"/home/jintac/jintac-nfvo/bin/pip2.7 install paramiko", "/home/jintac/jintac-nfvo/bin/pip2.7 install python-keystoneclient",
				"/home/jintac/jintac-nfvo/bin/pip2.7 install python-novaclient"]


    
    for cmd in cmd_list:
        print cmd
        status = commands.getoutput(cmd)
    print status
    return status


def clone_code(username, email, API_Key, API_KEY_SECRET,target_path):
    cmd1 = "git config --global user.name '%s'" % (username)
    print cmd1
    cmd2 = "git config --global user.email '%s'" % (email)
    print cmd2
    cmd3 = 'ssh-keygen -b 2048 -t rsa -f ~/.ssh/id_rsa -q -N "" -C "%s"' % (email)
    print cmd3
    cmd_lst = [cmd1, cmd2, cmd3]
    for cmd in cmd_lst:
        print cmd
        status = commands.getoutput(cmd)
        print status
    cmd4 = "cat ~/.ssh/id_rsa.pub"
    status = commands.getoutput(cmd4)
    json_strs = '{"key":"%s", "title":"%s"}' % (status, username)
    print json_strs
    
    cmd5 = """curl -i -X POST -H "X-Api-key: %s" -H "X-Api-secret: %s" -H "Content-type: application/json" -d '%s' --insecure https://api.assembla.com/v1/user/ssh_keys.json """ % (
        API_Key, API_KEY_SECRET, json_strs)
    status = commands.getoutput(cmd5)
    print status
    cmd6 = "git clone git@git.assembla.com:nfvo.git"
    print cmd6
    status = commands.getoutput(cmd6)
    

def run_app():
    
    cmd = "/root/Desktop/NFV/NFVO/bin/python2.7 /root/Desktop/nfvo/ngn_grid/manage.py runserver"
    print cmd
    status = commands.getoutput(cmd)
    return status


def script_help():
    parser = argparse.ArgumentParser()
    required = parser.add_argument_group('required arguments')
    required.add_argument("-u","--username",help="Provide assembla username",required=True)
    required.add_argument("-e","--email",help="Provide assembla email",required=True)
    required.add_argument("-k","--api_key",help="Provide assembla API key",required=True)
    required.add_argument("-s","--secret_api_key",help="Provide assembla Secret API key",required=True)
    parser.add_argument("-d","--directory_path",help="Path for creating Directory",default="/home/")
    parser.add_argument("-n","--directory_name",help="Name for directory",default="jintac")
    parser.add_argument("-v","--virtual_env_name",help="Name for the virtual env ",default="jintac-nfvo")
    
    args = parser.parse_args()
    return args

def main_func(args):
    flavor = chk_linux_flavor()
    version = chk_python_version()
    pkg_list = ['pip', 'virtualenv']
    dic_status = chk_pkg(pkg_list, flavor)
    username = args.username
    email = args.email
    API_Key = args.api_key
    API_KEY_SECRET = args.secret_api_key
    print "Required Argument are"
    print "USERNAME : " + args.username,"EMAIL : " + args.email,"APIKEY : " + args.api_key,"API_SECRET_KEY : " + args.secret_api_key
    print "Default arguments are "
    print "DIRECTORY_PATH : " + args.directory_path,"DIRECTORY_NAME : " + args.directory_name,"VIRTUAL_ENV_NAME : " + args.virtual_env_name
    for key, value in dic_status.items():
        if "not" in dic_status[key]:
            if 'CentOS' in flavor[0]:
                if dic_status[key] == "pip":
                    install_cmd = "yum"
                    print install_cmd
                else:
                    install_cmd = "pip"
                    print install_cmd
                pkg_name = dic_status[value]
                install_pkg(install_cmd, pkg_name)
            else:
                if dic_status[key] == "pip":
                    install_cmd = "apt-get"
                else:
                    install_cmd = "pip"
                pkg_name = dic_status[value]
                install_pkg(install_cmd, pkg_name)
                #else:
    print "aws"
    func = chk_pkg(pkg_list, flavor)
    directory_path = args.directory_path
    directory_name = args.directory_name
    virtual_env_name = args.virtual_env_name
    target_path = directory_path+ directory_name+virtual_env_name
    status = mkvirtual_env(directory_path,directory_name,virtual_env_name)
    status = clone_code(username, email, API_Key, API_KEY_SECRET,target_path)
    print status


if __name__ == "__main__":
    print "hello, starting to deploy the NFV !!"
    args = script_help()
    main_func(args)
    print "Yes, You are good to go !!"

