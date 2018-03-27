#!/usr/bin/env python2

from distutils.core import setup

setup(name='mitmproxy',
      version='0.1',
      packages=['mitmproxy'],
      scripts=[
        'extra/fencegenlog',
        'extra/fencetestlog',
        'extra/mitmproxy_wrapper',
        'scripts/mitm_turris_config.py',
        'mitmkeygen',
        'mitmlogdiff',
        'mitmlogview',
        'mitmproxy_http',
        'mitmproxy_snmp',
        'mitmproxy_ssh',
        'mitmproxy_ssl',
        'mitmproxy_telnet',
        'mitmreplay_http',
        'mitmreplay_snmp',
        'mitmreplay_ssh',
        'mitmreplay_ssl',
        'mitmreplay_telnet',
      ],
      data_files = [('/etc/init.d', ['initscripts/mitmproxy_wrapper'])],
     )
