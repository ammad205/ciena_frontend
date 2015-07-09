from django.shortcuts import HttpResponse, render_to_response, render
from  django.http.request import HttpRequest
import urllib, urllib2, json
import logging
from modeler_infra import configs
import time


def logs(request):
    return render_to_response('logs.html')



def get_logger(log_file=None,logger_name="default"):
    if log_file is None:
        log_file = configs.LOG_FILE
    logger = logging.getLogger(logger_name)
    handler = logging.FileHandler(log_file)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger
