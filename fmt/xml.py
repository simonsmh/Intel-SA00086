#!/usr/bin/env python
"""
Copyright (C) 2017, Intel Corporation. All rights reserved.

XML output routines
"""
import sys
import os.path
from tempfile import gettempdir
from time import gmtime, strftime
from common import messages
from common import glob

XML_FORMAT = '''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
<System>
    <Application_Name>%s</Application_Name>
    <Scan_Date>%s</Scan_Date>
    <Application_Version>%d.%d.%d.%d</Application_Version>
    <Computer_Name>%s</Computer_Name>
    <Hardware_Inventory>
        <Computer_Manufacturer>%s</Computer_Manufacturer>
        <Computer_Model>%s</Computer_Model>
        <OperatingSystem>%s</OperatingSystem>
        <Processor>%s</Processor>
    </Hardware_Inventory>
    <Firmware_Information>
        <Driver_Installed>%s</Driver_Installed>
        <FW_Version>%s</FW_Version>
        <Platform>%s</Platform>
        <SVN>%d</SVN>
    </Firmware_Information>
    <System_Status>
        <System_Risk>%s</System_Risk>
    </System_Status>
</System>'''

def report(hostname, manufacturer, model, processor, distribution,
           ver_str, family, svn, code, no_drv):
    '''Create XML report'''

    time = gmtime()
    name = "SA-00086-%s-%s.xml" % (hostname, strftime("%Y-%m-%d-%H-%M-%S", time))

    if code == glob.NOTVULNERABLE:
        risk = messages.MSG_NOT_VULNERABLE
    elif code == glob.HECI_NOT_INSTALLED:
        risk = messages.MSG_MAY_BE_DRIVER
    elif code == glob.HECI_ERROR:
        risk = messages.MSG_MAY_BE
    elif code == glob.DISCOVERY_VULNERABLE:
        risk = messages.MSG_VULNERABLE
    elif code == glob.DISCOVERY_NOT_VULNERABLE_PATCHED:
        risk = messages.MSG_PATCHED
    else:
        risk = messages.MSG_MAY_BE

    msg = XML_FORMAT % (messages.MSG_APP_NAME,
	                       strftime("%Y-%m-%d %H:%M:%S GMT", time),
                        glob.INTEL_SA_00086_VER_MAJOR,
                        glob.INTEL_SA_00086_VER_MINOR,
                        glob.INTEL_SA_00086_VER_PATCH,
                        glob.INTEL_SA_00086_VER_BUILD,
                        hostname,
                        manufacturer,
                        model,
                        distribution,
                        processor,
                        "False" if no_drv else "True",
                        ver_str,
                        glob.family2str(family),
                        svn,
                        risk)
    temp = None
    try:
        with open(name, "w") as the_file:
            the_file.write(msg)
    except IOError as the_exc:
        temp = gettempdir()
    if not temp:
        return
    try:
        filename = os.path.join(temp, name)
        with open(filename, "w") as the_file:
            the_file.write(msg)
        print "Report is placed at %s" % filename
    except IOError as the_exc:
        print >> sys.stderr, \
            "Failed to write to xml file %s: %s" % (the_exc.filename, the_exc.strerror)
