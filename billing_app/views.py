from django.shortcuts import HttpResponse, render_to_response, render
from  django.http.request import HttpRequest
import urllib, urllib2, json
from django.contrib.auth.decorators import login_required


@login_required
def billing(request):
    return render_to_response('billing.html')