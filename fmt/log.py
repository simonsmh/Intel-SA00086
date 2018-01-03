#!/usr/bin/env python
"""
Copyright (C) 2017, Intel Corporation. All rights reserved.

Log output routines"""
import sys
import os.path
from tempfile import gettempdir
from time import gmtime, strftime
from common import messages
from common import glob

STR_SYSTEM_INFO = messages.MSG_NAME + """ %s
""" + messages.MSG_MANUFACTURER + """ %s
""" + messages.MSG_MODEL + """ %s
""" + messages.MSG_PROC + """ %s
""" + messages.MSG_OS + """ %s
"""

STR_ME_INFO = messages.MSG_ENGINE + """ %s
""" + messages.MSG_FW_VERSION + """ %s
""" + messages.MSG_FW_SVN + """ %s
"""

STR_ME_INFO_SPS = messages.MSG_ENGINE + """ %s
""" + messages.MSG_FW_VERSION + """ %s
"""

class Log(object):
    '''Main logging interface'''
    def __init__(self, hostname):
        '''Start logging'''
        time = gmtime()
        self.temp_dir = None
        self.log_filename = "SA-00086-%s-%s.log" % \
                            (hostname, strftime("%Y-%m-%d-%H-%M-%S", time))
        try:
            self.log("Tool Started %s\n" % strftime("%Y-%m-%d %H:%M:%S GMT", time))
        except IOError as the_exc:
            self.temp_dir = gettempdir()
        if not self.temp_dir:
            return
        try:
            self.log_filename = os.path.join(self.temp_dir, self.log_filename)
            self.log("Tool Started %s\n" % strftime("%Y-%m-%d %H:%M:%S GMT", time))
        except IOError as the_exc:
            self.log_filename = None
            print >> sys.stderr, \
                "Failed to write to log file %s: %s" % (the_exc.filename, the_exc.strerror)

    def log(self, message):
        '''Log message to log'''
        if not self.log_filename: #not started
            return
        with open(self.log_filename, "a") as the_file:
            the_file.write(message)

    def log_system_info(self, hostname, manufacturer, model, processor, distribution):
        '''Log system information'''
        self.log(STR_SYSTEM_INFO % (hostname, manufacturer, model, processor,
                                    distribution))

    def log_me_info(self, family, ver_str, svn):
        '''Log ME information'''
        if family == glob.SPS:
            self.log(STR_ME_INFO_SPS % (glob.family2str(family), ver_str))
        else:
            self.log(STR_ME_INFO % (glob.family2str(family), ver_str, svn))

    def stop(self):
        '''Stop logging'''
        self.log("Tool Stopped\n")
        if self.temp_dir:
            print "Log is placed at %s" % self.log_filename
