#!/usr/bin/python
'''Returns a fact to indicate if this is a physical or virtual machine'''

# sysctl function by Michael Lynn
# https://gist.github.com/pudquick/581a71425439f2cf8f09
import plistlib
import subprocess

from ctypes import CDLL, c_uint, byref, create_string_buffer
from ctypes.util import find_library
libc = CDLL(find_library('c'))


def sysctl(name, isString=True):
    '''Wrapper for sysctl so we don't have to use subprocess'''
    size = c_uint(0)
    # Find out how big our buffer will be
    libc.sysctlbyname(name, None, byref(size), None, 0)
    # Make the buffer
    buf = create_string_buffer(size.value)
    # Re-run, but provide the buffer
    libc.sysctlbyname(name, buf, byref(size), None, 0)
    if isString:
        return buf.value
    else:
        return buf.raw


def is_virtual_machine():
    cpu_features = sysctl('machdep.cpu.features').split()
    return 'VMM' in cpu_features


def get_machine_type():
    '''Return the machine type: physical, vmware, parallels or
    unknown_virtual'''
    if not is_virtual_machine():
        return 'physical'

    # this is a virtual machine; see if we can tell which vendor
    try:
        proc = subprocess.Popen(['/usr/sbin/system_profiler', '-xml',
                                 'SPEthernetDataType', 'SPHardwareDataType'],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, err = proc.communicate()
        plist = plistlib.readPlistFromString(output)
        br_version = plist[1]['_items'][0]['boot_rom_version']
        if 'VMW' in br_version:
            return 'vmware'
        else:
            ethernet_vid = plist[0]['_items'][0]['spethernet_vendor-id']
            if '0x1ab8' in ethernet_vid:
                return 'parallels'

    except (IOError, KeyError, OSError):
        pass

    return 'unknown_virtual'


def fact():
    '''Return our physical_or_virtual fact'''
    return {'physical_or_virtual': get_machine_type()}


if __name__ == '__main__':
    print fact()
