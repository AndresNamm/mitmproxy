#!/usr/bin/env python

# Writes /etc/mitmproxy_wrapper.conf with configuration for current router

import os
import os.path
import sys
import re

from ConfigParser import SafeConfigParser

def getDefaultRouteIface():
    """ Returns name of interface for default route """
    lines = [l.rstrip() for l in file("/proc/net/route")]
    #first line is just heading
    for line in lines[1:]:
        parts = re.split(r"\s+", line)
        iface = parts[0]
        destination = parts[1]
        mask = parts[7]
        
        if destination == "00000000" and mask == "00000000":
            return iface

def fixListeningInterface(config_file):
    """ 
    Replace listening interface for empty string in config, which means listen on all interfaces. 
    """
    parser = SafeConfigParser()
    parser.read(config_file)
    parser.set("wrapper", "interface", "")
    with open(config_file, "w") as cfg_fileobj:
        parser.write(cfg_fileobj)
    

config_file = "/etc/mitmproxy_wrapper.conf"

# don't overwrite existing config
# 2015-07-27 - fix interface if config file exists because we hit the dumb
#   firewall script generation bug which causes the firewall redirect rule not to
#   work
if os.path.isfile(config_file):
    fixListeningInterface(config_file)
    sys.exit(0)

serial = os.popen("/usr/bin/atsha204cmd serial-number").read().rstrip()

basePort = 10000

configBase = \
"""
[wrapper]
mitmproxy_executable = /usr/bin/mitmproxy_ssh
pidfile = /var/mitmproxy_wrapper.pid
interface = %s
logfile = /dev/null
loglevel = debug
daemonize = true

[mitmproxy]
target_host = 217.31.192.112
target_port = %d
local_port = 58732
turris_id = %016x
tty_log = /dev/null
"""

try:
    serial = int(serial, 16)
except ValueError:
    print >> sys.stderr, "Cannot convert serial number to hex"
    sys.exit(2)

if not (serial >= 0x0000000500000002 and serial <= 0x0000000500002E5F) and \
    not (serial >= 0x0000000900000008 and serial <= 0x0000000900002E65) and \
    not (serial >= 0x0000000a00000004 and serial <= 0x0000000a00000369) and \
    not (serial >= 0x0000000b00000000 and serial <= 0x0000000b000157b5):
        print >> sys.stderr, "Serial out of range"
        sys.exit(3)

if not serial % 11 == 0:
    print >> sys.stderr, "Serial not divisible by 11"

# 00000005xxx series
if (serial >= 0x0000000500000002 and serial <= 0x0000000500002E5F):
    port = basePort + (serial - 0x0000000500000002)//11
# 00000009xxx series
elif (serial >= 0x0000000900000008 and serial <= 0x0000000900002E65):
    port = basePort + 1080 + (serial - 0x0000000900000008)//11
# 0000000axxx series
elif (serial >= 0x0000000a00000004 and serial <= 0x0000000a00000369):
    port = basePort + 2160 + (serial - 0x0000000a00000004)//11
# 0000000bxxx series
elif (serial >= 0x0000000b00000000 and serial <= 0x0000000b000157b5):
    port = basePort + 2240 + (serial - 0x0000000b00000000)//11

# Let's not use default route iface, since we are on special port anyway
# It works better with buggy firewall redirect scripts
#iface = getDefaultRouteIface()
iface = ""

with open(config_file, "w") as config:
    config.write(configBase % (iface, port, serial))

