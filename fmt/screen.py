#!/usr/bin/env python
"""
Copyright (C) 2017, Intel Corporation. All rights reserved.

Screen output routines
"""
from time import gmtime, strftime
from common import messages
from common import glob

STR_HEADER = messages.MSG_APP_NAME + """
Copyright(C) 2017, Intel Corporation, All rights reserved

""" + messages.MSG_APP_VER + """ %d.%d.%d.%d
""" + messages.MSG_SCAN_DATE + """ %s
"""

STR_ME_INFO = """*** """ + messages.MSG_ME_INFO + """ ***
""" + messages.MSG_ENGINE + """ %s
""" + messages.MSG_FW_VERSION + """ %s
""" + messages.MSG_FW_SVN + """ %s
"""

STR_ME_INFO_SPS = """*** """ + messages.MSG_ME_INFO + """ ***
""" + messages.MSG_ENGINE + """ %s
""" + messages.MSG_FW_VERSION + """ %s
"""

STR_SYSTEM_INFO = """*** """ + messages.MSG_SYS_INFO + """ ***
""" + messages.MSG_NAME+ """ %s
""" + messages.MSG_MANUFACTURER + """ %s
""" + messages.MSG_MODEL + """ %s
""" + messages.MSG_PROC + """ %s
""" + messages.MSG_OS + """ %s
"""

STR_RISK_VULNERABLE = """*** """ + messages.MSG_RISK_ASSESSMENT + """ ***
""" + messages.MSG_BASED + " " + messages.MSG_VULNERABLE + """
""" + messages.MSG_EXPLANATION + """
""" + messages.MSG_EXPLANATION_LONG + """
"""

STR_RISK_VULNERABLE_PATCHED = """*** """ + messages.MSG_RISK_ASSESSMENT + """ ***
""" + messages.MSG_BASED + " " + messages.MSG_PATCHED + """
"""

STR_RISK_NOT_VULNERABLE = """*** """ + messages.MSG_RISK_ASSESSMENT + """ ***
""" + messages.MSG_BASED + " " + messages.MSG_NOT_VULNERABLE + """
"""

STR_RISK_UNKNOWN = """*** """ + messages.MSG_RISK_ASSESSMENT + """ ***
""" + messages.MSG_MAY_BE + """
"""

STR_RISK_DRIVER = """*** """ + messages.MSG_RISK_ASSESSMENT + """ ***
""" + messages.MSG_MAY_BE_DRIVER + """
"""

STR_NEED_ROOT = messages.MSG_PRIV + """
"""

STR_FOOTER = messages.MSG_FOOTER + """
"""

def print_header():
    '''Print header'''
    print STR_HEADER % (glob.INTEL_SA_00086_VER_MAJOR,
                        glob.INTEL_SA_00086_VER_MINOR,
                        glob.INTEL_SA_00086_VER_PATCH,
                        glob.INTEL_SA_00086_VER_BUILD,
                        strftime("%Y-%m-%d %H:%M:%S GMT", gmtime()))

def print_system_info(hostname, manufacturer, model, processor, distribution):
    '''Print system information'''
    print STR_SYSTEM_INFO % (hostname, manufacturer, model, processor,
                             distribution)

def print_me_info(family, ver_str, svn):
    '''Print ME information'''
    if family == glob.SPS:
        print STR_ME_INFO_SPS % (__family2fullstr(family), ver_str)
    else:
        print STR_ME_INFO % (__family2fullstr(family), ver_str, svn)

def __family2fullstr(family):
    '''Family to full string'''
    if family == glob.ME:
        return messages.MSG_EXPLANATION_ENG_ME
    elif family == glob.TXE:
        return messages.MSG_EXPLANATION_ENG_TXE
    elif family == glob.SPS:
        return messages.MSG_EXPLANATION_ENG_SPS
    elif family == glob.UNKNOWN:
        return messages.MSG_EXPLANATION_ENG_ME

def print_vulnerable(family):
    '''Print vulnerable status'''
    print STR_RISK_VULNERABLE % __family2fullstr(family)

def print_not_vulnerable():
    '''Print not vulnerable status'''
    print STR_RISK_NOT_VULNERABLE

def print_vulnerable_patched():
    '''Print vulnerable patched status'''
    print STR_RISK_VULNERABLE_PATCHED

def print_unknown():
    '''Print unknown status'''
    print STR_RISK_UNKNOWN

def print_driver():
    '''Print driver needed status'''
    print STR_RISK_DRIVER

def print_need_root():
    '''Print elevated privileges message'''
    print STR_NEED_ROOT

def print_risk(family, code):
    '''Print risk message'''
    if code == glob.NOTVULNERABLE:
        print_not_vulnerable()
    elif code == glob.HECI_NOT_INSTALLED:
        print_driver()
    elif code == glob.HECI_ERROR:
        print_unknown()
    elif code == glob.DISCOVERY_VULNERABLE:
        print_vulnerable(family)
    elif code == glob.DISCOVERY_NOT_VULNERABLE_PATCHED:
        print_vulnerable_patched()
    else:
        print_unknown()

def print_footer():
    '''Print footer'''
    print STR_FOOTER
