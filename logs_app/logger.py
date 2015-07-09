__author__ = "Awais Ali, Usman Khan"
__copyright__ = "Copyright 2015, Logging Library for ngnGridProject"
__maintainer__ = "Awais Ali"
__email__ = "awais.ali@jintac.com"
__status__ = "Development"

###############################################################################
# Logging Framework
#
# This file contains the initial implementation of library code
# for ngnGrid's logging framework. Ideally, this should be a re-usable
# module and each separate module shouyld instatntiate a separate object
# for its own logging needs. Eahc logging file will be of this format:
# <logging_dir>/<module_name><timestamp>.log
# Where logging_dir is usually /var/log/ on unix systems.
#
# Example usage:
# x = Logger("moduleFoo").getLoggerWithConsole()
# x.debug("Foo")
###############################################################################

#########
# Imports
#########
import logging
import time
import sys

#########
# Globals
#########
dir_path = "/var/log"

#
# Main implementation of Logger class
#
class Logger():
    #
    # Constructor Implentation
    # This will get the logger file and handler instantiated.
    # It is very basic config. We can expand on it if need be.
    #
    def __init__(self, module_name):
        try:
            inst_time = "%s" % (time.strftime("%H%M%S-%d%m%Y"))
            file_name = "%s/%s-%s.log" % (dir_path, module_name, inst_time)
            logging.basicConfig(filename=file_name,level=logging.DEBUG,
                    format='%(asctime)s %(message)s')
            self.logger = logging.getLogger(module_name)
        except:
            print "Unable to instantiate logger:", sys.exc_info()[0]
            raise
    #
    # This function when called, will return logger with an extra handler
    # for handling console output. Useful for debugging on console.
    #
    def getLoggerWithConsole(self):
        ch = logging.StreamHandler()
        self.logger.addHandler(ch)
        return self.logger

    #
    # Get the logger object
    #
    def getLogger(self):
        return self.logger

