#!/usr/bin/env python
"""
Copyright (C) 2017, Intel Corporation. All rights reserved.

mkhi helper functions for mei driver
"""
import os
import errno
import select
import struct
import mei

UUID = '8e6a6715-9abc-4043-88ef-9e39c6f63e0f'
FIXED_UUID = '55213584-9a29-4916-badf-0fb7ed682aeb'

def connect(mei_fd):
    '''Connect to dynamic MKHI client'''
    return mei.connect(mei_fd, UUID)

def connect_fixed(mei_fd):
    '''Connect to fixed MKHI client'''
    return mei.connect(mei_fd, FIXED_UUID)

VER_SIZE_SPS = 20
VER_SIZE = 28
VER_SIZE_MAX = max(VER_SIZE_SPS, VER_SIZE)
ARB_SIZE = 1076

def req_fw_ver(mei_fd):
    '''Send FW version request'''
    buf_write = struct.pack("I", 0x000002FF)
    return os.write(mei_fd, buf_write)

def fw_ver_parse(buf_read):
    '''Parse FW version'''
    if len(buf_read) == VER_SIZE:
        str_ver = struct.unpack("4BH2B2HH2B2HH2B2H", buf_read)
    elif len(buf_read) == VER_SIZE_SPS:
        str_ver = struct.unpack("4BH2B2HH2B2H", buf_read)
    else:
        raise IOError(errno.EMSGSIZE, "Wrong version message size")
    return str_ver

def get_fw_ver_str(mei_fd):
    '''Read FW version'''
    rlist, _, _ = select.select([mei_fd], [], [], 5)
    if not rlist:
        raise IOError(errno.ETIME, os.strerror(errno.ETIME) + "in mkhi.get_fw_info")
    buf = os.read(mei_fd, VER_SIZE_MAX)
    return fw_ver_parse(buf)

def fw_ver(mei_fd):
    '''Read FW version'''
    req_fw_ver(mei_fd)
    return get_fw_ver_str(mei_fd)

def req_arb_status(mei_fd):
    '''Send ARB status request'''
    buf_write = struct.pack("I", 0x0000020C)
    return os.write(mei_fd, buf_write)

def arb_status_parse(buf_read):
    '''Parse ARB status'''
    if len(buf_read) != ARB_SIZE:
        raise IOError(errno.EMSGSIZE,
                      "Wrong ARB status message size %d" % len(buf_read))
    return struct.unpack("4B4I128I128I4I4I", buf_read)

def get_arb_status(mei_fd):
    '''Read ARB status'''
    rlist, _, _ = select.select([mei_fd], [], [], 5)
    if not rlist:
        raise IOError(errno.ETIME, os.strerror(errno.ETIME) + "in mkhi.get_arb_status")
    buf = os.read(mei_fd, ARB_SIZE)
    return arb_status_parse(buf)

def arb_status(mei_fd):
    '''Receive ARB status'''
    req_arb_status(mei_fd)
    return get_arb_status(mei_fd)
