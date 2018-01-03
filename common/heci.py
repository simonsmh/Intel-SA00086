#!/usr/bin/env python
"""
Copyright (C) 2017, Intel Corporation. All rights reserved.
"""
import os
import errno
import time
import mei
import mei.mkhi
import mei.fwu
from mei.debugfs import fixed_address_soft
from common import glob

def get_mkhi_fd():
    '''Find device with MKHI client'''
    for dev_node in mei.dev_list():
        mei_fd = mei.open_dev(dev_node)
        try:
            mei.mkhi.connect(mei_fd)
        except IOError as err:
            os.close(mei_fd)
            if err.errno != errno.ENOTTY:
                continue
        else:
            return mei_fd
        time.sleep(0.1)
        mei_fd = mei.open_dev(dev_node)
        try:
            fixed_address_soft(dev_node, True)
            mei.mkhi.connect_fixed(mei_fd)
        except IOError as err:
            os.close(mei_fd)
        else:
            return mei_fd

    raise IOError(errno.ENOENT, "No device with MKHI found", "/dev/mei*")

def get_fwu_fd():
    '''Find device with FWU client'''
    for dev_node in mei.dev_list():
        mei_fd = mei.open_dev(dev_node)
        try:
            mei.fwu.connect(mei_fd)
        except IOError:
            os.close(mei_fd)
        else:
            return mei_fd

    raise IOError(errno.ENOENT, "No device with FWU found", "/dev/mei*")

def is_supported_version(fw_ver):
    '''Check if FW version is in supported list'''
    if not fw_ver[6]:
        if fw_ver[5] in [6, 7, 8, 9, 10, 11]:
            family = glob.ME
            return True, family
        elif fw_ver[5] == 3:
            family = glob.TXE
            return True, family
        else:
            family = glob.UNKNOWN
    else:
        family = glob.SPS
        if fw_ver[5] == 4 or fw_ver[10] == 4:
            return True, family
    return False, family

def is_old_me(fw_ver):
    '''Check if FW version is in the old ME list'''
    return fw_ver[5] in [6, 7, 8, 9, 10]

def is_old_me_vulnerable(fw_ver):
    '''Check if old FW version is vulnerable'''
    vers = [fw_ver[5], fw_ver[4], fw_ver[8], fw_ver[7]]
    if vers[0] == 6 or vers[0] == 7:
        return True
    if vers[0] == 8:
        return vers < [8, 1, 72, 3002]
    if vers[0] == 9:
        if vers[1] == 0 or vers[1] == 1:
            return vers < [9, 1, 42, 3002]
        elif vers[1] == 5:
            return vers < [9, 5, 61, 3012]
    if vers[0] == 10:
        return vers < [10, 0, 56, 3002]
    #Can't be
    return True

def get_fw_ver():
    '''Get FW version from device'''
    try:
        mei_fd = get_mkhi_fd()
        fw_ver = mei.mkhi.fw_ver(mei_fd)
        os.close(mei_fd)
    except IOError as the_err:
        if the_err.errno == errno.ENOENT:
            raise
        mei_fd = get_fwu_fd()
        fw_ver = mei.fwu.fw_ver_as_mkhi(mei_fd)
        os.close(mei_fd)
    return fw_ver

def get_txe_svn():
    '''Get TXE SVN from device'''
    mei_fd = get_mkhi_fd()
    arb = mei.mkhi.arb_status(mei_fd)
    os.close(mei_fd)
    return arb[11] if arb[11] != 0 else arb[139]

def get_me_svn():
    '''Get ME SVN from device'''
    mei_fd = get_fwu_fd()
    info = mei.fwu.fw_info(mei_fd)
    os.close(mei_fd)
    return info[51]

def get_image_type():
    '''Get image type from device'''
    mei_fd = get_fwu_fd()
    image = mei.fwu.get_image_type(mei_fd)
    os.close(mei_fd)
    return image

def get_fw_state():
    """Calculate FW state"""
    fw_ver = get_fw_ver()

    ret, family = is_supported_version(fw_ver)
    if not ret:
        svn = 0
        code = glob.NOTVULNERABLE
    elif family == glob.TXE:
        svn = get_txe_svn()
        if svn < 3:
            code = glob.DISCOVERY_VULNERABLE
        else:
            code = glob.DISCOVERY_NOT_VULNERABLE_PATCHED
    elif family == glob.ME:
        if is_old_me(fw_ver):
            svn = 0
            image = get_image_type()
            if image == mei.fwu.IMAGE_TYPE_FULL:
                if is_old_me_vulnerable(fw_ver):
                    code = glob.DISCOVERY_VULNERABLE
                else:
                    code = glob.DISCOVERY_NOT_VULNERABLE_PATCHED
            else:
                code = glob.NOTVULNERABLE
        else:
            svn = get_me_svn()
            if svn < 3:
                code = glob.DISCOVERY_VULNERABLE
            else:
                code = glob.DISCOVERY_NOT_VULNERABLE_PATCHED
    elif family == glob.SPS:
        svn = 0
        if fw_ver[8] < 4 or fw_ver[13] < 4:
            code = glob.DISCOVERY_VULNERABLE
        else:
            code = glob.DISCOVERY_NOT_VULNERABLE_PATCHED
    else:
        svn = 0
        code = glob.DISCOVERY_UNKNOWN

    if family == glob.SPS:
        ver_str = "%d %d.%d.%d.%d %d %d.%d.%d.%d" % (fw_ver[6], fw_ver[5],
                                                     fw_ver[4], fw_ver[8], fw_ver[7],
                                                     fw_ver[11], fw_ver[10],
                                                     fw_ver[9], fw_ver[13], fw_ver[12])
    else:
        ver_str = "%d.%d.%d.%d" % (fw_ver[5], fw_ver[4], fw_ver[8], fw_ver[7])

    return ver_str, code, family, svn
