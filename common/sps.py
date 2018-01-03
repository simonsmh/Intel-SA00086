#!/usr/bin/env python
"""
Copyright (C) 2017, Intel Corporation. All rights reserved.

SPS tool runner
"""
from os import path
import subprocess
import errno
from common import glob

class SPSError(Exception):
    '''Base class for SPS tool exceptions'''
    pass

class SPSToolError(SPSError):
    '''SPS tool errors'''
    def __init__(self, ret):
        SPSError.__init__(self)
        self.ret = ret

class SPSUnsupportedError(SPSError):
    '''Platform is unsupported'''
    pass

class SPSVerNotFound(SPSError):
    '''No version found'''
    pass

class SPSNoTool(SPSError):
    '''Can't execute tool'''
    pass

def run_tool(use_old=False):
    '''Run SPSInfo tool'''
    try:
        if use_old:
            command = [path.join(path.dirname(__file__), "spsInfoLinux64_3"), "-NOCOLORS"]
        else:
            command = [path.join(path.dirname(__file__), "spsInfoLinux64"), "-NOCOLORS"]
        process = subprocess.Popen(command, stdout=subprocess.PIPE)
        info, _ = process.communicate()
        retcode = process.poll()
        if retcode == 244:
            raise SPSUnsupportedError()
        if retcode:
            raise SPSToolError(retcode)
        info = info.strip()
        opr_ver = ""
        rec_ver = ""
        for line in info.split("\n"):
            if "SPS Image FW version" in line:
                ver0 = line.split(':')[1].split(',')
                ver1 = ver0[1].strip().split(' ')[0]
                ver2 = ver0[0].strip().split(' ')[0]
                opr_ver = ver1.split('.')
                rec_ver = ver2.split('.')
                break
        if not opr_ver or not rec_ver:
            raise SPSVerNotFound()
    except OSError as the_err:
        if the_err.errno == errno.ENOENT:
            raise SPSNoTool()
        raise

    if int(opr_ver[0]) != 4 and int(rec_ver[0]) != 4:
        code = glob.NOTVULNERABLE
    else:
        if int(opr_ver[2]) < 4 or int(rec_ver[2]) < 4:
            code = glob.DISCOVERY_VULNERABLE
        else:
            code = glob.DISCOVERY_NOT_VULNERABLE_PATCHED
    family = glob.SPS
    ver_str = "%s.%s.%s.%s (Operational) %s.%s.%s.%s (Recovery)" % \
              (opr_ver[0], opr_ver[1], opr_ver[2], opr_ver[3],
               rec_ver[0], rec_ver[1], rec_ver[2], rec_ver[3])

    return ver_str, code, family
