#!/usr/bin/env python
"""
Copyright (C) 2017, Intel Corporation. All rights reserved.

mei module
"""
import array
import fcntl
import os
import uuid
import struct
import sys
import time
import errno

DEF_DEV_NAMES = ["mei0", "mei", "mei1", "mei2", "mei3"]
def to_dev(name):
    """return device path by device name"""
    return "/dev/%s" % name

def dev_default_name():
    """return default mei device name"""
    for dev_name in DEF_DEV_NAMES:
        if os.access(to_dev(dev_name), os.F_OK):
            return dev_name

    raise IOError(errno.ENOENT, "No device found", "/dev/mei*")

def dev_default():
    """return default mei device string"""
    for devnode in [to_dev(s) for s in DEF_DEV_NAMES]:
        if os.access(devnode, os.F_OK):
            return devnode

    raise IOError(errno.ENOENT, "No device found", "/dev/mei*")

def open_dev(devnode):
    '''open mei device'''
    return os.open(devnode, os.O_RDWR)

def open_dev_default():
    '''open default mei device'''
    devnode = dev_default()
    return os.open(devnode, os.O_RDWR)

def dev_list():
    '''generate list of existing mei devices'''
    for dev_name in DEF_DEV_NAMES:
        if os.access(to_dev(dev_name), os.F_OK):
            yield to_dev(dev_name)

IOCTL_MEI_CONNECT_CLIENT = 0xc0104801
def connect(mei_fd, uuid_str):
    '''connect to client with provided uuid'''
    cl_uuid = uuid.UUID(uuid_str)
    buf = array.array('b', cl_uuid.bytes_le)
    fcntl.ioctl(mei_fd, IOCTL_MEI_CONNECT_CLIENT, buf, 1)
    maxlen, vers = struct.unpack("<IB", buf.tostring()[:5])
    # print("connected %s, maxlen %x, vers %x" % (uuid_str, maxlen, vers))

    return maxlen, vers
