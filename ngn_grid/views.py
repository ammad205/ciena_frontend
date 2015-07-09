#from mx.Tools.Tools import username
from django.shortcuts import HttpResponse, render_to_response, render, HttpResponseRedirect
from  django.http.request import HttpRequest
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views,authenticate,login
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.contrib import auth
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from ngn_grid.models import *
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
import requests, json, yaml


def create_user(request):
    user = User.objects.create_user("aamir", 'aamir@gmail.com', 'password')
    user.save()



def login_user(request):

    print "123"
    print "123123123123123123123"
    if request.method == "POST":
        # request.session['user'] = user_list[0].username
        print "working"

        username1 = request.REQUEST["username"]
        password2 = request.REQUEST["password"]
        user = authenticate(username=username1, password=password2)

        if user is not None:
            if user.is_active:
                auth.login(request, user)
                request.session['user']=user
                print "!!!!!!!!!!!!!!!!!!!!!!",request.session["user"]
                return HttpResponseRedirect('/dashboard')
            else:
                return render(request, 'login.html')
        else:
            return render(request, 'login.html')
    return render(request, 'login.html')


@login_required
def index(request):


    # if 'user' not in request.session:
    #     user_list = Users.objects.all()
    #     return render(request, 'login.html', {'users_list' : user_list} )


    return render_to_response('index.html',context_instance=RequestContext(request))

def dashboard(request):

    return render('dashboard.html' )

def panel(request):
    return render('panel.html', context_instance=RequestContext(request))

def authentication(request):
    user_list = Users.objects.all()
    request.session['user'] = user_list[0].username
    print request.session['user']
    return render(request, 'login.html', {'users_list' : user_list} )


def logout(request):
    views.logout(request)
    return HttpResponseRedirect("/login")


def my_view(request):
    username = request.GET['username']
    password = request.GET['password']
    user = authenticate(username=username, password=password)
    print user
    print password
    if user is not None:
        if user.is_active:
            login(request, user)
            # Redirect to a success page.
        else:
            print "user inactive"
    else:
        print "no user"

@csrf_exempt
def ammad(request):
    curr_state  = vms.objects.filter(datacenter_id=request.POST['datacentername'])
    data = serializers.serialize('json', list(curr_state))
    print type(data),"afdafaaaaaaaaaa"
    return HttpResponse(data, content_type='application/json')


@csrf_exempt
def ammad2(request):
    print "llllsslsl"
    data ={"auth": {"tenantName": "admin","passwordCredentials": {"username": "admin","password": "Yahoo.com!!"}}}
    url = "http://192.168.7.225:5000/v2.0/tokens";
    headers = { "Content-Type": "application/json","Accept": "application/json","User-Agent": "python-keystoneclient"}
    res = requests.post(url=url, headers=headers,data=json.dumps(data))
    a = yaml.load(res.content)
    url2 = "http://192.168.7.225:8774/v1.1/f214455038e14721adb8631a3191ba77/images/detail"
    headers2 = {'X-Auth-Project-Id': 'admin', 'User-Agent': 'python-novaclient', 'Content-Type': 'application/json','Accept': 'application/json', 'X-Auth-Token': a['access']['token']['id']}
    res2 = requests.get(url=url2, headers=headers2)
    b = yaml.load(res2.content)

    print type(json.dumps(b)),"afdafaaaaaaaaaa"

    result = json.dumps(b, ensure_ascii=False)
    return HttpResponse(result, content_type='application/json')

from django.db.models import Q

@csrf_exempt
def spawn(request):
    #print request.meta
    token_url = "http://192.168.7.225:5000/v2.0/tokens";
    token_data ={"auth": {"tenantName": "admin","passwordCredentials": {"username": "admin","password": "Yahoo.com!!"}}}
    token_headers = { "Content-Type": "application/json","Accept": "application/json","User-Agent": "python-keystoneclient"}
    res = requests.post(url=token_url, headers=token_headers,data=json.dumps(token_data))
    token_response = yaml.load(res.content)
    #print request.META['HTTP_D_NAME']
    #print request.POST['a']
    a=json.loads(request.POST['a'])
    print a
    spawn_api_url="http://10.91.0.20:8774/v2.1/ebe2dfb299674faca3a244bc99db02ab/servers"
    spawn_api_header = {'X-Auth-Project-Id': 'admin','User-Agent': 'python-novaclient','Content-Type': 'application/json','Accept': 'application/json','X-Auth-Token': token_response['access']['token']['id']}
    spawn_api_json={"server": {"name": "test-vmlist-api", "imageRef": "8e7f2897-7e6e-4228-9943-b144b7c6e392", "flavorRef": "1", "max_count": 1, "min_count": 1, "availability_zone":"datacenter3", "networks": [{"uuid":"8d9c26e6-a74c-4160-9289-e822efd597f1"}], "security_groups": [{"name": "default"}]}}

    pope =int(request.META['HTTP_D_NAME'])
    if pope == 1:
        spawn_api_json['server']['availability_zone']='datacenter3'
    elif pope==2:
        spawn_api_json['server']['availability_zone']='nova'
    else:
        spawn_api_json['server']['availability_zone']='nova'
    print spawn_api_json
    for i in a:
       spawn_api_json['server']['imageRef']=i['id']
       #spawn_api_json['server']['availability_zone']=request.META['HTTP_D_NAME']
       spawn_api_json['server']['name']=i['name']
       for x in range(0, int(i['value'])):
           print "http//:www.spawn.com/"+request.META['HTTP_D_NAME']+"/"+i['id']
           #print spawn_api_json
           #print spawn_api_header
           #res2=requests.post(url=spawn_api_url, headers=spawn_api_header,data=json.dumps(spawn_api_json))
           print res
           #b = Blog(name='Beatles Blog', tagline='All the latest Beatles news.')
           v=vms(datacenter_id=request.META['HTTP_D_NAME'],name=i['name'])
           v.save()
    return HttpResponse('heloo')

@csrf_exempt
def connect(request):
    curr_state  = Datacenter.objects.filter(~Q(id = request.POST['datacentername']))
    data = serializers.serialize('json', list(curr_state))
    print type(data),"afdafaaaaaaaaaa"
    return HttpResponse(data, content_type='application/json')


@csrf_exempt
def connect2(request):
    print request.META['HTTP_D_NAME']
    print request.POST['a']
    a=json.loads(request.POST['a'])
    print a[0]['ip']
    return HttpResponse(request, content_type='application/json')

