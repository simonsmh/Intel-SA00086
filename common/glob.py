#!/usr/bin/env python
"""
Copyright (C) 2017, Intel Corporation. All rights reserved.

Global defines
"""

#Version
INTEL_SA_00086_VER_MAJOR = 1
INTEL_SA_00086_VER_MINOR = 0
INTEL_SA_00086_VER_PATCH = 0
INTEL_SA_00086_VER_BUILD = 152
#'''Vulnerability status'''
NOTVULNERABLE = 0
HECI_NOT_INSTALLED = 10
HECI_ERROR = 11
DISCOVERY_VULNERABLE = 100
DISCOVERY_NOT_VULNERABLE_PATCHED = 101
DISCOVERY_UNKNOWN = 200

def status2str(status):
    '''Status to string'''
    if status == NOTVULNERABLE:
        return "NOTVULNERABLE"
    elif status == HECI_NOT_INSTALLED:
        return "HECI_NOT_INSTALLED"
    elif status == HECI_ERROR:
        return "HECI_ERROR"
    elif status == DISCOVERY_VULNERABLE:
        return "DISCOVERY_VULNERABLE"
    elif status == DISCOVERY_NOT_VULNERABLE_PATCHED:
        return "DISCOVERY_NOT_VULNERABLE_PATCHED"
    elif status == DISCOVERY_UNKNOWN:
        return "DISCOVERY_UNKNOWN"

#'''FW family'''
ME = 0
TXE = 1
SPS = 2
UNKNOWN = 3

def family2str(family):
    '''Family to string'''
    if family == ME:
        return "Intel(R) ME"
    elif family == TXE:
        return "Intel(R) TXE"
    elif family == SPS:
        return "Intel(R) SPS"
    elif family == UNKNOWN:
        return "UNKNOWN"
