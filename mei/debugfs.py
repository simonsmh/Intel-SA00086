#!/usr/bin/env python
"""
Copyright (C) 2017, Intel Corporation. All rights reserved.

debugfs interface for mei driver
"""
import codecs
import os
import re

def open_file_read(path, encoding='UTF-8'):
    '''Open specified file read-only'''
    try:
        orig = codecs.open(path, 'r', encoding)
    except Exception:
        raise

    return orig

def valid_path(path):
    '''Valid path'''
    # No relative paths
    msg = "Invalid path: %s" % (path)
    if not path.startswith('/'):
        print "%s (relative)" % (msg)
        return False

    if '"' in path:  # We double quote elsewhere
        print "%s (contains quote)" % (msg)
        return False

    try:
        os.path.normpath(path)
    except Exception:
        print "%s (could not normalize)" % (msg)
        return False

    return os.path.exists(path)

def check_for_debugfs(device):
    """Finds and returns the mountpoint for mei None otherwise"""

    filesystem = '/proc/filesystems'
    mounts = '/proc/mounts'
    support_debugfs = False
    regex_debugfs = re.compile(r'^\S+\s+(\S+)\s+debugfs\s')
    mei_dir = None

    if valid_path(filesystem):
        with open_file_read(filesystem) as f_in:
            for line in f_in:
                if 'debugfs' in line:
                    support_debugfs = True

    if not support_debugfs:
        return False

    if valid_path(mounts):
        with open_file_read(mounts) as f_in:
            for line in f_in:
                match = regex_debugfs.search(line)
                if match:
                    mountpoint = match.groups()[0] + '/' +  os.path.basename(device)
                    if not valid_path(mountpoint):
                        return False
                    mei_dir = mountpoint

    # Check if meclients are present
    if not valid_path(mei_dir + '/meclients'):
        mei_dir = None
    return mei_dir

def fixed_address(device, allow):
    '''Toggle fixed_address driver knob'''
    mei_dir = check_for_debugfs(device)
    if not mei_dir:
        return

    with open(mei_dir + '/allow_fixed_address', 'r+') as allow_f:
        if allow:
            allow_f.write('Y')
        else:
            allow_f.write('N')

def fixed_address_soft(device, allow):
    '''(Dis)allow fixed address client on old HW only'''

    if get_fa_support(device):
        return

    fixed_address(device, allow)

def get_devstate(device):
    """Parse mei devstate"""

    devstate = {}
    hbm = {}
    mei_dir = check_for_debugfs(device)
    if not mei_dir:
        raise Exception("Can't connect to debugfs")

    with open_file_read(mei_dir + '/devstate') as f_in:
        base = 0
        for line in f_in:
            values = line.strip('\n').split(':')
            if base == 0:
                if values[0] == "hbm features":
                    base = 1
                    continue
                devstate[values[0]] = values[1].strip()
            elif base == 1:
                if values[0] == "pg":
                    devstate["pg_enabled"] = values[1].split(',')[0].strip()
                    devstate["pg_state"] = values[1].split(',')[1].strip()
                    continue
                hbm[values[0].strip()] = values[1].strip()
    return devstate, hbm

def get_fa_support(device):
    '''Return FW support for fixed-address clients'''
    _, hbm = get_devstate(device)
    return int(hbm.get('FA', '0'))
