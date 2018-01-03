#!/usr/bin/env python
"""
Copyright (C) 2017, Intel Corporation. All rights reserved.

fwu helper functions for mei driver
"""
import os
import errno
import select
import struct
import mei

UUID = '309dcde8-ccb1-4062-8f78-600115a34327'
VER_SIZE_6 = 48
VER_SIZE_7 = 52
VER_SIZE_8 = 56
VER_SIZE_MAX = max(VER_SIZE_6, VER_SIZE_7, VER_SIZE_8)

def connect(mei_fd):
    '''Connect to FWU client'''
    return mei.connect(mei_fd, UUID)

def req_fw_info(mei_fd):
    '''Send FW info request'''
    buf_write = struct.pack("I", 0x0000001E)
    return os.write(mei_fd, buf_write)

def fw_info_parse(buf_read):
    '''Parse FW info'''
    if len(buf_read) != 456:
        raise IOError(errno.EMSGSIZE,
                      "Wrong FW info message size %d" % len(buf_read))
    return struct.unpack("4I4H4H2I32B7I4H2I16BH4B2I32B4H4H12II3IH48I", buf_read)

#SVN is at 51

def get_fw_info(mei_fd):
    '''Read FW info'''
    rlist, _, _ = select.select([mei_fd], [], [], 5)
    if not rlist:
        raise IOError(errno.ETIME, os.strerror(errno.ETIME) + "in fwu.get_fw_info")
    buf = os.read(mei_fd, 10000)
    return fw_info_parse(buf)

def fw_info(mei_fd):
    '''Receive FW info'''
    req_fw_info(mei_fd)
    return get_fw_info(mei_fd)

def req_fw_ver(mei_fd):
    '''Send FW version request'''
    buf_write = struct.pack("I", 0x00000000)
    return os.write(mei_fd, buf_write)

def get_fw_ver_raw(mei_fd):
    '''Read raw FW version'''
    rlist, _, _ = select.select([mei_fd], [], [], 5)
    if not rlist:
        raise IOError(errno.ETIME, os.strerror(errno.ETIME) + "in fwu.get_fw_ver")
    buf_read = os.read(mei_fd, VER_SIZE_MAX)
    return buf_read

def fw_ver_parse(buf_read):
    '''Parse FW version'''
    if len(buf_read) == VER_SIZE_6:
        str_ver = struct.unpack("7I4H4H2H", buf_read)
    elif len(buf_read) == VER_SIZE_7:
        str_ver = struct.unpack("7I4H4H2HI", buf_read)
    elif len(buf_read) == VER_SIZE_8:
        str_ver = struct.unpack("7I4H4H2HII", buf_read)
    else:
        raise IOError(errno.EMSGSIZE, "Wrong version message size")
    return str_ver

def get_fw_ver_str(mei_fd):
    '''Read FW version'''
    buf = get_fw_ver_raw(mei_fd)
    return fw_ver_parse(buf)

def fw_ver(mei_fd):
    '''Obtain FW version'''
    req_fw_ver(mei_fd)
    return get_fw_ver_str(mei_fd)

def fw_ver_as_mkhi(mei_fd):
    '''Obtain FW version formatted as mkhi version'''
    ver = fw_ver(mei_fd)
    return [0, 0, 0, 0, ver[8], ver[7], 0, ver[10], ver[9], 0, 0, 0, 0, 0]

def req_platform_type(mei_fd):
    '''Send platform type request'''
    buf_write = struct.pack("I", 0x0000000E)
    return os.write(mei_fd, buf_write)

def get_platform_type_raw(mei_fd):
    '''Read raw platform type'''
    rlist, _, _ = select.select([mei_fd], [], [], 5)
    if not rlist:
        raise IOError(errno.ETIME, os.strerror(errno.ETIME) + "in fwu.get_platform_type")
    buf_read = os.read(mei_fd, 12)
    return buf_read

def platform_type_parse(buf_read):
    '''Parse platform type'''
    return struct.unpack("3I", buf_read)

def get_platform_type_str(mei_fd):
    '''Read platform type'''
    buf = get_platform_type_raw(mei_fd)
    return platform_type_parse(buf)

#'''List of possible image types'''
IMAGE_TYPE_NO_SKU = 0x0
IMAGE_TYPE_SLIM = 0x2
IMAGE_TYPE_SMALL = 0x3
IMAGE_TYPE_FULL = 0x4
IMAGE_TYPE_TEST = 0xF

def get_image_type(mei_fd):
    '''Obtain image type'''
    req_platform_type(mei_fd)
    platf = get_platform_type_str(mei_fd)
    return (platf[2] & 0x0F00) >> 8
