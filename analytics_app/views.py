from django.shortcuts import HttpResponse, render_to_response, render
from  django.http.request import HttpRequest
import urllib, urllib2, json, datetime, time
from django.contrib.auth.decorators import login_required
from httplib import HTTPConnection
from django.views.decorators.csrf import csrf_exempt

#server_ip = "http://192.168.7.225:8081"
server_ip = "http://localhost:8081"


@login_required
def analyticsDashboard(request):
    return render_to_response('analytics_dashboard.html')
@login_required
def analytics(request):
    return render_to_response('analytics.html')

def testrun(request):
    return render_to_response('testrun.html')
def dashboard(request):
    return render_to_response('dashboard.html')
# function for handling get requests
#@login_required
def get_url_data(url_str):
    url = urllib.urlopen(url_str + '?flat')

    try:
        raw_data = json.loads(url.read())
        return json.dumps(raw_data)
    except Exception,e:
        print "exception",e

# function for handling post requests
#@login_required
def post_url_data(url_str, data):
    req = urllib2.Request(url_str)
    req.add_header('Content-Type', 'application/json')
    response = urllib2.urlopen(req, json.dumps(data))
    httpResp = HttpResponse(response.read())
    #print httpResp.content
    return httpResp

# function for handling all types of request requests
# and then multiplexes them based on their type
#@login_required
def generic(request):
    assert isinstance(request, HttpRequest)
    # checks if the request is a get or post request
    if request.method == 'GET':
        print request.path
        print server_ip+request.path
        try:
            url_data = get_url_data(server_ip + request.path)
            return HttpResponse(url_data,content_type='application/json')
        except Exception,e:
            print e
    elif request.method == 'POST':
        #print request.body + "body"
        url_data = post_url_data(server_ip + request.path,request.body)
        return HttpResponse(url_data,content_type='application/json')
