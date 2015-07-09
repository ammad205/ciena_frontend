__author__ = 'bilalahmed'
from django.shortcuts import HttpResponse, render_to_response, render
from  django.http.request import HttpRequest
import urllib, urllib2, json, datetime, time
from django.contrib.auth.decorators import login_required
from httplib import HTTPConnection
from django.views.decorators.csrf import csrf_exempt
import requests,sys,socket

#server_ip = "http://192.168.7.225:8081"
server_ip = "http://localhost:8081"
openstackTokenID = ""

def getVMUpTime(request):
    url = "http://117.20.30.70:8774/v3/e1c1806c-2e92-4dc1-ab51-5b8ddee38ec9/os-simple-tenant-usage/e1c1806c-2e92-4dc1-ab51-5b8ddee38ec9"
    resp = urllib2.urlopen(urllib2.Request(url, headers={'Authorization': requestAuthToken(request)}))
    return resp


def getTokenID(request):
    if openstackTokenID == "":
        token = requestAuthToken(request)
        if "token" in token: 
	    if "user" in token["token"]:
		if "id" in token["token"]["user"]:
            	  return token["token"]["user"]["id"]
    else: return openstackTokenID
    return ""


def requestAuthToken(request):
    queryStr = """{"auth":{"identity":{"methods":["password"],"password":{"user":{"name":"admin","domain":{"id":"default"},"password": "Jintac123"}}}}}"""
    queryJS = json.loads(queryStr)
    queryJS["auth"]["identity"]["password"]["user"]["name"] = "admin"
    queryJS["auth"]["identity"]["password"]["user"]["password"] = "Jintac123"
    #FIXME add dynamic ip address with port
    return post_url_data("http://117.20.30.70:5000/v3/auth/tokens", queryJS)


# returns the total ingress traffic for the last 24 hours
def getlast24hoursIng(request):
    currentTime = datetime.datetime.now()
    fT = unix_time_micro(currentTime)
    iT = unix_time_micro(currentTime - datetime.timedelta(1))
    queryStr = """{"table":"FlowSeriesTable","start_time":0,"end_time":0,"select_fields":["flow_class_id","direction_ing","sum(bytes)","sum(packets)"],"limit":150000,"dir":1}"""
    queryJS = json.loads(queryStr)
    queryJS["start_time"] = iT
    queryJS["end_time"] = fT
    return post_url_data(server_ip + "/analytics/query", queryJS)

# returns the total egress traffic for the last 24 hours
def getlast24hoursEg(request):
    currentTime = datetime.datetime.now()
    fT = unix_time_micro(currentTime)
    iT = unix_time_micro(currentTime - datetime.timedelta(1))
    queryStr = """{"table":"FlowSeriesTable","start_time":0,"end_time":0,"select_fields":["flow_class_id","direction_ing","sum(bytes)","sum(packets)"],"limit":150000,"dir":0}"""
    queryJS = json.loads(queryStr)
    queryJS["start_time"] = iT
    queryJS["end_time"] = fT
    return post_url_data(server_ip + "/analytics/query", queryJS)

# gets the total network data usage for a given network
def getNetworkDataUsage(request):
    network_name = request.path.split('/',-1)[-1]
    data = get_url_data(server_ip + '/analytics/uves/virtual-network/' + network_name)
    dataJS = json.loads(data)
    result = { 'name':network_name }
    if 'UveVirtualNetworkAgent' in dataJS:
        if 'in_bytes' in dataJS['UveVirtualNetworkAgent']:
            result['in_bytes'] = dataJS['UveVirtualNetworkAgent']['in_bytes']
        else:
            result['in_bytes'] = 0
        if 'out_bytes' in dataJS['UveVirtualNetworkAgent']:
            result['out_bytes'] = dataJS['UveVirtualNetworkAgent']['out_bytes']
        else:
            result['out_bytes'] = 0
    else:
        result['in_bytes'] = 0
        result['out_bytes'] = 0
    return HttpResponse(json.dumps(result),content_type='application/json')

# gets the total bandwidth usage for a given network
def getNetworkBandwidthUsage(request):
    network_name = request.path.split('/',-1)[-1]
    data = get_url_data(server_ip + '/analytics/uves/virtual-network/' + network_name)
    dataJS = json.loads(data)
    result = { 'name':network_name }
    if 'UveVirtualNetworkAgent' in dataJS:
        if 'in_bandwidth_usage' in dataJS['UveVirtualNetworkAgent']:
            result['in_bandwidth_usage'] = dataJS['UveVirtualNetworkAgent']['in_bandwidth_usage']
        else:
            result['in_bandwidth_usage'] = 0
        if 'out_bandwidth_usage' in dataJS['UveVirtualNetworkAgent']:
            result['out_bandwidth_usage'] = dataJS['UveVirtualNetworkAgent']['out_bandwidth_usage']
        else:
            result['out_bandwidth_usage'] = 0
    else:
        result['in_bandwidth_usage'] = 0
        result['out_bandwidth_usage'] = 0
    return HttpResponse(json.dumps(result),content_type='application/json')

# gets the total flow count for a given network
def getNetworkFlowCount(request):
    network_name = request.path.split('/',-1)[-1]
    data = get_url_data(server_ip + '/analytics/uves/virtual-network/' + network_name)
    dataJS = json.loads(data)
    result = { 'name':network_name }
    if 'UveVirtualNetworkAgent' in dataJS:
        if 'egress_flow_count' in dataJS['UveVirtualNetworkAgent']:
            result['egress_flow_count'] = dataJS['UveVirtualNetworkAgent']['egress_flow_count']
        else:
            result['egress_flow_count'] = 0
        if 'ingress_flow_count' in dataJS['UveVirtualNetworkAgent']:
            result['ingress_flow_count'] = dataJS['UveVirtualNetworkAgent']['ingress_flow_count']
        else:
            result['ingress_flow_count'] = 0
    else:
        result['egress_flow_count'] = 0
        result['ingress_flow_count'] = 0
    return HttpResponse(json.dumps(result),content_type='application/json')

# gets the total flow count for a given network
def getNetworkPacketCount(request):
    network_name = request.path.split('/',-1)[-1]
    data = get_url_data(server_ip + '/analytics/uves/virtual-network/' + network_name)
    dataJS = json.loads(data)
    result = { 'name':network_name }
    if 'UveVirtualNetworkAgent' in dataJS:
        if 'in_tpkts' in dataJS['UveVirtualNetworkAgent']:
            result['in_tpkts'] = dataJS['UveVirtualNetworkAgent']['in_tpkts']
        else:
            result['in_tpkts'] = 0
        if 'out_tpkts' in dataJS['UveVirtualNetworkAgent']:
            result['out_tpkts'] = dataJS['UveVirtualNetworkAgent']['out_tpkts']
        else:
            result['out_tpkts'] = 0
    else:
        result['in_tpkts'] = 0
        result['out_tpkts'] = 0
    return HttpResponse(json.dumps(result),content_type='application/json')

# returns the total seconds since epoch for a given time
def unix_time(dt):
    epoch = datetime.datetime.utcfromtimestamp(0)
    delta = dt - epoch
    return delta.total_seconds()

# returns the total micro-seconds since epoch for a given time
def unix_time_micro(dt):
    return int(unix_time(dt) * 1000000.0)

def get_url_data(url_str):
    url = urllib.urlopen(url_str + '?flat')
    raw_data = json.loads(url.read())
    return json.dumps(raw_data)

# function for handling post requests
def post_url_data(url_str, data):
    req = urllib2.Request(url_str)
    req.add_header('Content-Type', 'application/json')
    response = urllib2.urlopen(req, json.dumps(data))
    httpResp = HttpResponse(response.read())
    return httpResp

# gets all the network analytics parameters for a given network
def getNetworkStats(request):
    network_name = request.path.split('/',-1)[-1]
    data = get_url_data(server_ip + '/analytics/uves/virtual-network/' + network_name)
    dataJS = json.loads(data)
    result = { 'name':network_name }
    if 'UveVirtualNetworkAgent' in dataJS:
        if 'in_bytes' in dataJS['UveVirtualNetworkAgent']:
            result['in_bytes'] = dataJS['UveVirtualNetworkAgent']['in_bytes']
        else:
            result['in_bytes'] = 0
        if 'out_bytes' in dataJS['UveVirtualNetworkAgent']:
            result['out_bytes'] = dataJS['UveVirtualNetworkAgent']['out_bytes']
        else:
            result['out_bytes'] = 0
    else:
        result['in_bytes'] = 0
        result['out_bytes'] = 0

    if 'UveVirtualNetworkAgent' in dataJS:
        if 'in_bandwidth_usage' in dataJS['UveVirtualNetworkAgent']:
            result['in_bandwidth_usage'] = dataJS['UveVirtualNetworkAgent']['in_bandwidth_usage']
        else:
            result['in_bandwidth_usage'] = 0
        if 'out_bandwidth_usage' in dataJS['UveVirtualNetworkAgent']:
            result['out_bandwidth_usage'] = dataJS['UveVirtualNetworkAgent']['out_bandwidth_usage']
        else:
            result['out_bandwidth_usage'] = 0
    else:
        result['in_bandwidth_usage'] = 0
        result['out_bandwidth_usage'] = 0

    if 'UveVirtualNetworkAgent' in dataJS:
        if 'egress_flow_count' in dataJS['UveVirtualNetworkAgent']:
            result['egress_flow_count'] = dataJS['UveVirtualNetworkAgent']['egress_flow_count']
        else:
            result['egress_flow_count'] = 0
        if 'ingress_flow_count' in dataJS['UveVirtualNetworkAgent']:
            result['ingress_flow_count'] = dataJS['UveVirtualNetworkAgent']['ingress_flow_count']
        else:
            result['ingress_flow_count'] = 0
    else:
        result['egress_flow_count'] = 0
        result['ingress_flow_count'] = 0

    if 'UveVirtualNetworkAgent' in dataJS:
        if 'in_tpkts' in dataJS['UveVirtualNetworkAgent']:
            result['in_tpkts'] = dataJS['UveVirtualNetworkAgent']['in_tpkts']
        else:
            result['in_tpkts'] = 0
        if 'out_tpkts' in dataJS['UveVirtualNetworkAgent']:
            result['out_tpkts'] = dataJS['UveVirtualNetworkAgent']['out_tpkts']
        else:
            result['out_tpkts'] = 0
    else:
        result['in_tpkts'] = 0
        result['out_tpkts'] = 0

    return HttpResponse(json.dumps(result),content_type='application/json')

# gets the statistics for the given vm for the last hour
def getVMStats(request):
    vm_name = request.path.split('/',-1)[-1]
    print vm_name
    try:
        data = get_url_data(server_ip + '/analytics/uves/virtual-machine/' + vm_name)
        dataJS = json.loads(data)
        result = {'name': vm_name ,'cpu_usage':0, 'total_memory':0, 'used_memory':0, 'in_bw_usage':0, 'in_bytes':0, 'in_pkts':0, 'out_bw_usage':0, 'out_bytes':0, 'out_pkts':0}
    except Exception,e:
        print e

    if 'UveVirtualMachineAgent' in dataJS:
	if 'cpu_info' in dataJS['UveVirtualMachineAgent']:
		if 'cpu_one_min_avg' in dataJS['UveVirtualMachineAgent']['cpu_info']:
			result['cpu_usage'] = dataJS['UveVirtualMachineAgent']['cpu_info']['cpu_one_min_avg']
		if 'vm_memory_quota' in dataJS['UveVirtualMachineAgent']['cpu_info']:
			result['total_memory'] = dataJS['UveVirtualMachineAgent']['cpu_info']['vm_memory_quota']/1024
		if 'rss' in dataJS['UveVirtualMachineAgent']['cpu_info']:
			result['used_memory'] = dataJS['UveVirtualMachineAgent']['cpu_info']['rss']/1024

    if 'VirtualMachineStats' in dataJS:
        if 'if_stats' in dataJS['VirtualMachineStats']:
            interfaces_list = dataJS['VirtualMachineStats']['if_stats'] # it is a list of interfaces list
            for interfaces in interfaces_list: # traversing the list of interfaces
                if 'StatTable.VirtualMachineStats.if_stats' in interfaces:
                    for interface in interfaces['StatTable.VirtualMachineStats.if_stats']: # loop for traversing each interface
                        if 'SUM(if_stats.in_bw_usage)' in interface:
                            result['in_bw_usage'] += interface['SUM(if_stats.in_bw_usage)']
                        if 'SUM(if_stats.in_bytes)' in interface:
                            result['in_bytes'] += interface['SUM(if_stats.in_bytes)']
                        if 'SUM(if_stats.in_pkts)' in interface:
                            result['in_pkts'] += interface['SUM(if_stats.in_pkts)']
                        if 'SUM(if_stats.out_bw_usage)' in interface:
                            result['out_bw_usage'] += interface['SUM(if_stats.out_bw_usage)']
                        if 'SUM(if_stats.out_bytes)' in interface:
                            result['out_bytes'] += interface['SUM(if_stats.out_bytes)']
                        if 'SUM(if_stats.out_pkts)' in interface:
                            result['out_pkts'] += interface['SUM(if_stats.out_pkts)']

    return HttpResponse(json.dumps(result),content_type='application/json')
