from django.shortcuts import HttpResponse, render_to_response, render
from  django.http.request import HttpRequest
import urllib, urllib2, json
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from ngn_grid.models import *
from django.contrib import auth
from django.template import RequestContext
from modeler_infra.pyOrchestrateLib import FireFly
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import ast

@login_required
def nfvHome(request):
    return render_to_response('nfvo_home.html', context_instance=RequestContext(request))


def n2fvHome(request):
    return render_to_response('2/nfvo_home.html', context_instance=RequestContext(request))


def nfvIndex(request):
    return render_to_response('nfvo-index.html', context_instance=RequestContext(request))

def nfvPanel(request):
    return render_to_response('nfvo-panel.html', context_instance=RequestContext(request))

def policyBuilder(request):
    return render_to_response('policy-builder.html')

def nfvActiveTopology(request):
    return render_to_response('nfvo-active-topology.html')

def nfvDropBox(request):
    return render_to_response('drop-images-box.html')

def userHistoryData(request):
    task_data=''
    try:
        task_serial = serializers.serialize('json', task_history.objects.filter(username=request.session['user']))
        print type(task_serial)
        task_result = json.loads(task_serial)
        task_data = json.dumps(task_result)
    except Exception,e:
        print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>",e
    return HttpResponse(task_data, content_type='application/json')

def serviceMonitoring(request):
    instance_name = task_history.objects.all()
    return render( request, 'service-monitoring.html', {'instance_name':instance_name})
result2 = ''
result1 = ''
def processTest(request):
    firewall_name = task_history.objects.all()
    firewall = firewall_name[0].instance_name
    import ping
    main_obbj = ping.getPingStatus(firewall)
    result1, result2, result3 = main_obbj.getLatestStatus(firewall)
    print "1233123>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
    print result1, result2, result3
    
    # if result2 == "Avaliable":
    #     if result1 == "NotActive":
    #         red_light = "led-red"
    #         green_light = "led-green"
    #         return render_to_response(request,'diaggnostic.html',{'red_light':red_light, 'green_light':green_light})
    #     elif result1 == "Active":
    #         red_light = "led-red"
    #         green_light = "led-green"
    #         return render_to_response(request,'diaggnostic.html',{'green_light':green_light,'red_light':red_light})
    # else:
    #     green_light = "led-green"
    #     red_light = "led-red"
    #     return render_to_response(request,'diaggnostic.html',{'red_light':red_light,'green_light':green_light})
    #return render_to_response('diaggnostic.html',{'firewall_result': 'Avaliable' , 'internet_result':'NotActive'})
    return HttpResponse()



@csrf_exempt
def userHistory(request):
    #current_user = request.session['user']
    tt = task_history.objects.create(username=request.session['user'], instance_name=request.POST['instance_name'], telnet=request.POST['telnet'], ssh=request.POST['ssh'], netconf=request.POST['netconf'], left_interface=request.POST['left_ntwrk'], right_interface=request.POST['right_ntwrk'], mng_interface=request.POST['mngt_ntwrk'])


    return HttpResponse()

@csrf_exempt
def deleteUserData(request):
    delete_data = task_history.objects.filter(instance_name=request.POST['instance'])
    delete_data.delete()
    return HttpResponse()

@csrf_exempt
def diagnostic(request):
        firewall_name = task_history.objects.all()
        print "abc"
        firewall = firewall_name[0].instance_name
        print "abcdddd"
        import ping
        main_obbj = ping.getPingStatus(firewall)
        result1, result2, result3 = main_obbj.getLatestStatus(firewall)
        print "abcaaaaa", result3, result2, result1
        vm_name = request.POST['instance_name1']
        print vm_name
        locate = request.POST['location1']
        print "111111111 ", locate
        return render_to_response('diaggnostic.html',{'vm_name':vm_name,'location':locate,'firewall_result':result2, 'internet_result':result1 })


@csrf_exempt
def spawnModeler(request):
    import ast
    from collections import OrderedDict
    aList = []
    if(request.POST['telnet']=="true"):{ aList.append("telnet") };
    if(request.POST['ssh']=="true"):{ aList.append("ssh") };
    if(request.POST['netconf']=="true"):{ aList.append("netconf") };
    json_str = '{"username":"admin","password":"Jintac123","tenant":"admin","commands":["netconf","ssh"],"nics":[{"mngt_ntwrk":"svc-vn-mgmt","left_ntwrk":"DMZ","right_ntwrk":"kq-be"}]}'

    json_str2 = {"vm_name":request.POST['instance_name'] ,"username":"admin","password":"Jintac123","tenant":"admin","commands":aList,"nics":[{"mngt_ntwrk":request.POST['mngt_ntwrk'],"left_ntwrk":request.POST['left_ntwrk'],"right_ntwrk":request.POST['right_ntwrk']}]};

    order_dict =  dict(OrderedDict([('body', json_str2), ('ttl', 5000)]))
    import pubsub_infra.test_queue
    main_obj = pubsub_infra.test_queue.queueClass()
    data = main_obj.postMessage(order_dict)
    return HttpResponse()

    
    
@csrf_exempt
def deleteOpenstackVM(request):
    vm_name = request.POST['instance']
    fun = Functions()
    #nova = fun.validate_token(username, password, tenant)
    #add credentials from config file, not hard coding it here, but let it be for the time being
    nova = Client(1.1, 'admin', 'secret123', 'admin', 'http://192.168.7.10:5000/v2.0')
    try:
        server = nova.servers.find(name=vm_name)
        server.delete()
    except Exception, e:
        return HttpResponse(e)

    return HttpRequest()

def queue(request):
    import ast
    from collections import OrderedDict
    #json_str ="{'body': {'username':'admin','password':'Jintac123','tenant':'admin','commands':['netconf','ssh'],'nics':[{'mngt_ntwrk':'svc-vn-mgmt','left_ntwrk':'DMZ','right_ntwrk':'kq-be'}]}, 'ttl': 50000}"
    #json_str = '{"username":"admin","password":"Jintac123","tenant":"admin","commands":["netconf","ssh"],"nics":[{"mngt_ntwrk":"svc-vn-mgmt","left_ntwrk":"DMZ","right_ntwrk":"kq-be"}]}'
    json_str = "{'username':'admin','password':'Jintac123','tenant':'admin','commands':['netconf','ssh'],'nics':[{'mngt_ntwrk':'svc-vn-mgmt','left_ntwrk':'DMZ','right_ntwrk':'kq-be'}]}"
    msg = ast.literal_eval(json_str)
    order_dict =  dict(OrderedDict([('body', json_str), ('ttl', 5000)]))

    import pubsub_infra.test_queue
    main_obj = pubsub_infra.test_queue.queueClass()
    data = main_obj.postMessage(order_dict)
    return HttpResponse(data)

def PB(request):
    return render_to_response('PB/nfvo_home.html')

