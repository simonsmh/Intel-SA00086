#!/usr/bin/env python
"""
Copyright (C) 2017, Intel Corporation. All rights reserved.

SA-00086 Detection Tool
"""
import os
import sys
import re
import errno
from socket import gethostname
from platform import linux_distribution
import fmt.screen
from fmt.log import Log
import fmt.xml
from common.heci import get_fw_state
from common import sps
from common import glob

def gethost():
    '''Extract host name'''
    try:
        return gethostname()
    except:
        return "NA"

def processor():
    '''Extract first processor name'''
    try:
        with open("/proc/cpuinfo", 'r') as the_file:
            info = the_file.read().strip()
        for line in info.split("\n"):
            if "model name" in line:
                return re.sub(".*model name.*:", "", line, 1).strip()
    except:
        return "N/A"

def manufacturer():
    '''Extract manufacturer'''
    try:
        with open("/sys/class/dmi/id/sys_vendor", 'r') as the_file:
            info = the_file.read().strip()
        return info
    except:
        return "N/A"

def model():
    '''Extract model'''
    try:
        with open("/sys/class/dmi/id/product_name", 'r') as the_file:
            info = the_file.read().strip()
        return info
    except:
        return "N/A"

def distribution():
    '''Format distribution'''
    try:
        return ' '.join([str(x) for x in linux_distribution()]) + ' (' + os.uname()[2] + ')'
    except:
        return "N/A"

def main():
    """Main routine"""

    log = Log(gethost())
    fmt.screen.print_header()
    fmt.screen.print_system_info(gethost(), manufacturer(),
                                    model(), processor(),
                                    distribution())
    log.log_system_info(gethost(), manufacturer(),
                               model(), processor(),
                               distribution())
    try:
        ver_str, code, family, svn = get_fw_state()
    except (OSError, IOError) as the_err:
        if the_err.errno == errno.ENOENT:
            code = glob.HECI_NOT_INSTALLED
        else:
            code = glob.HECI_ERROR
        if the_err.errno == errno.EACCES:
            fmt.screen.print_need_root()
        ver_str = "N/A"
        family = glob.UNKNOWN
        svn = 0
        log.log("HECI error: %s[%d]\n" %
                       (the_err.strerror, the_err.errno))

    no_drv = True if code == glob.HECI_NOT_INSTALLED else False
    if no_drv:
        try:
            ver_str, code, family = sps.run_tool()
        except sps.SPSUnsupportedError as the_err:
            try:
                ver_str, code, family = sps.run_tool(use_old=True)
            except sps.SPSUnsupportedError:
                log.log("SPS tool meet unsupported platform\n")
            except sps.SPSNoTool as the_err:
                log.log("Can't find SPS tool\n")
            except sps.SPSToolError as the_err:
                log.log("SPS tool returned error %d\n" % the_err.ret)
            except sps.SPSVerNotFound as the_err:
                log.log("Can't find SPS version in the tool output\n")
            except OSError as the_err:
                log.log("SPS tool failed with error %s[%d]\n" %
                               (the_err.strerror, the_err.errno))
        except sps.SPSNoTool as the_err:
            log.log("Can't find SPS tool\n")
        except sps.SPSToolError as the_err:
            log.log("SPS tool returned error %d\n" % the_err.ret)
        except sps.SPSVerNotFound as the_err:
            log.log("Can't find SPS version in the tool output\n")
        except OSError as the_err:
            log.log("SPS tool failed with error %s[%d]\n" %
                           (the_err.strerror, the_err.errno))

    if code != glob.HECI_ERROR and code != glob.HECI_NOT_INSTALLED:
        fmt.screen.print_me_info(family, ver_str, svn)
        log.log_me_info(family, ver_str, svn)

    fmt.screen.print_risk(family, code)
    log.log("Status: %s\n" % glob.status2str(code))

    fmt.xml.report(gethost(), manufacturer(),
                      model(), processor(), distribution(),
                      ver_str, family, svn, code, no_drv)

    fmt.screen.print_footer()
    log.stop()
    return code

if __name__ == '__main__':
    sys.exit(main())
