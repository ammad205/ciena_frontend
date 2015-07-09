__author__ = 'bilalahmed'

from django.http.request import HttpRequest
from django.shortcuts import HttpResponse
from django.shortcuts import render_to_response
import json


class DummyData:
    # function which processes requests
    def process_request(self, request):
        assert isinstance(request, HttpRequest)
        print(request.path)
        #self.process_post_request(request)
        if request.method == 'GET':
            return self.process_get_request(request.path)
        elif request.method == 'POST':
            return self.process_post_request(request)

    # function which processes get requests
    def process_get_request(self, path):
        if path == "/analytics/uves/virtual-machines":
            return render_to_response('dummy/virtual_machines',content_type='application/json')
        elif "virtual-machine" in path:
            print('dummy/' + path.split("e/")[1])
            return render_to_response('dummy/' + path.split("e/")[1],content_type='application/json')


    #FIXME
    queryStr = """{"table":"FlowSeriesTable","start_time":1412228400000000,"end_time":1412230200000000,"select_fields":["flow_class_id","direction_ing","T","T=600","protocol","sum(bytes)","sum(packets)"],"sort_fields":["T"],"sort":2,"limit":150000,"where":[[{"name":"sourcevn","value":"default-domain:demo:BE-VN","op":1},{"name":"sourceip","value":"250.250.1.5","op":1},{"name":"protocol","value":"1","op":1}],[{"name":"sourcevn","value":"default-domain:demo:BE-VN","op":1},{"name":"sourceip","value":"30.30.30.30","op":1},{"name":"protocol","value":"1","op":1}]],"dir":1}"""


    # function which processes post requests
    def process_post_request(self, request):
        #print(request.body)
        #queryJS = json.loads(self.queryStr)
        queryJS = json.loads(request.body)
        if "T=600" in queryJS["select_fields"]:
            return self.get_granular_data(queryJS,"600")
        elif "T=1200" in queryJS["select_fields"]:
            return self.get_granular_data(queryJS,"1200")
        elif "T=1800" in queryJS["select_fields"]:
            return self.get_granular_data(queryJS,"1800")
        else:
            return HttpResponse('{"value": []}',content_type='application/json')

    # function which processes granular data queries
    def get_granular_data(self,queryJS,grain):
        ip,protocol = "", ""
        if "where" in queryJS:
            for condition in queryJS["where"][0]:
                if condition["name"] == 'sourceip':
                    ip = condition['value']
                elif condition["name"] == 'protocol':
                    protocol = condition['value']
                if ip != "" and protocol != "":
                    #print(ip + " " + protocol)
                    #print render_to_response('dummy/' + protocol + "/" + grain + "/" +  ip + "_" + grain + "_" + protocol,content_type='application/json').content
                    return render_to_response('dummy/' + protocol + "/" + grain + "/" +  ip + "_" + grain + "_" + protocol,content_type='application/json')
            if ip == "" or protocol == "":
                return HttpResponse('{"value": []}',content_type='application/json')
        else:
            return HttpResponse('{"value": []}',content_type='application/json')


    def process_query(self, query):
        print(query)



