__author__ = 'aamir_raza'

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
                    "python2.7 /root/Desktop/get-pip.py", "pip2.7 install virtualenv"]
                for cmd in install_cmd:
                    status = commands.getoutput(cmd)
                    print cmd
                #status = commands.getoutput(install_cmd)
                print status
        dic_status[pkg_name] = status
        cmd = "pip2.7 install virtualenv"
        print "Virtual ENV", cmd
        statuse = commands.getoutput(cmd)
        print statuse
        #print dic_status
        print status
    return dic_status


def install_pkg(install_cmd, pkg_name):
    cmd = "%s install %s" % (instll_cmd, pkg_name)
    status = commands.getoutput(cmd)
    print status
    return status


def mkvirtual_env():
    #cmd_list = ["mkdir /home/NFV","virtualenv /home/NFV/NFVO"," source /home/NFV/NFVO/bin/activate"]
    cmd_list = ["mkdir /root/Desktop/NFV", "virtualenv-2.7 /root/Desktop/NFV/NFVO",
                " source /root/Desktop/NFV/NFVO/bin/activate",
                "/root/Desktop/NFV/NFVO/bin/pip2.7 install Django==1.7.1", "pip2.7 install mysql-python"]
    for cmd in cmd_list:
        print cmd
        status = commands.getoutput(cmd)
    print status
    return status


def clone_code(username, email, API_Key, API_KEY_SECRET):
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
    #cmd5 = """curl -i -X POST -H "X-Api-key: 2b914f51ba6fecfb83cd" -H "X-Api-secret: 151e88cc4cbcc9f8f012fbdb389afb36a6f6ee5d" -H "Content-type: application/json" -d '%s' --insecure https://api.assembla.com/v1/user/ssh_keys.json """%(json_strs)
    cmd5 = """curl -i -X POST -H "X-Api-key: %s" -H "X-Api-secret: %s" -H "Content-type: application/json" -d '%s' --insecure https://api.assembla.com/v1/user/ssh_keys.json """ % (
        API_Key, API_KEY_SECRET, json_strs)
    status = commands.getoutput(cmd5)
    print status
    cmd6 = "git clone git@git.assembla.com:nfvo.git"
    print cmd6
    status = commands.getoutput(cmd6)


def run_app():
    #cmd = "/home/NFV/NFVO/bin/python2.7 /home/nfvo/manage.py runserver"
    cmd = "/root/Desktop/NFV/NFVO/bin/python2.7 /root/Desktop/nfvo/ngn_grid/manage.py runserver"
    print cmd
    status = commands.getoutput(cmd)
    return status


def main_func():
    flavor = chk_linux_flavor()
    version = chk_python_version()
    pkg_list = ['pip', 'virtualenv']
    dic_status = chk_pkg(pkg_list, flavor)
    username = "razaaamir"
    email = "aamir.raza@jintac.com"
    API_Key = "2b914f51ba6fecfb83cd"
    API_KEY_SECRET = "151e88cc4cbcc9f8f012fbdb389afb36a6f6ee5d"
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
    status = mkvirtual_env()
    status = clone_code(username, email, API_Key, API_KEY_SECRET)
    status = run_app()
    print status


if __name__ == "__main__":
    print "hello"
    main_func()
    print "hi"

