#!/usr/local/munki/munki-python
import objc
import re
from Foundation import NSBundle, NSURL, NSURLSession


kIOMasterPortDefault = 0
kIOPlatformSerialNumberKey = "IOPlatformSerialNumber"
kCFAllocatorDefault = None
NSURLSessionTaskStateCompleted = 3
dataTaskResponse = None

IOKit_bundle = NSBundle.bundleWithIdentifier_('com.apple.framework.IOKit')

functions = [("IOServiceGetMatchingService", b"II@"),
             ("IOServiceMatching", b"@*"),
             ("IORegistryEntryCreateCFProperty", b"@I@@I"),
            ]

objc.loadBundleFunctions(IOKit_bundle, globals(), functions)

def io_key(keyname):
    platform_expert = IOServiceGetMatchingService(kIOMasterPortDefault, IOServiceMatching(b"IOPlatformExpertDevice"))
    return IORegistryEntryCreateCFProperty(platform_expert, keyname, kCFAllocatorDefault, 0)

def get_hardware_serial():
    return io_key(kIOPlatformSerialNumberKey)

def completionHandler(data, response, error):
    global dataTaskResponse
    dataTaskResponse = data

def get_claws_hostname(serial):
    session = NSURLSession.sharedSession()
    url = NSURL.URLWithString_(f"https://claws.rit.edu/s2h/{serial}")
    task = session.dataTaskWithURL_completionHandler_(url, completionHandler)
    task.resume()
    while task.state() != NSURLSessionTaskStateCompleted:
        pass
    while dataTaskResponse is None:
        pass
    return str(dataTaskResponse, 'utf-8')
    # return urllib.request.urlopen("https://claws.rit.edu/s2h/serialLookup.php?Serial={}".format(serial)).read()

def is_registered(r):
    if re.match('.*\.rit\.edu.',r) is not None:
        return True
    else:
        return False

def fact():
    serial = get_hardware_serial()
    claws_hostname = get_claws_hostname(serial)
    registered = is_registered(claws_hostname)
    hostname = claws_hostname.rstrip('.') if registered else ''
    '''Return our is_registered fact'''
    return {'is_claws_registered': registered,
            'claws_hostname': hostname
            }

if __name__ == '__main__':
    print(fact())
