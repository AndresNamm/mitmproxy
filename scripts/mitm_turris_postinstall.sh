#!/bin/sh

fatal() {
    echo "$@"
    exit 1
}

opkg update
opkg install mitmproxy || fatal "Cannot install mitmproxy"

#Allow port 22 from wan
uci add firewall rule
uci set "firewall.@rule[-1].name=Allow-SSH-wan"
uci set "firewall.@rule[-1].src=wan"
uci set "firewall.@rule[-1].target=ACCEPT"
uci set "firewall.@rule[-1].proto=tcp"
uci set "firewall.@rule[-1].dest_port=22"
uci commit firewall
/sbin/fw3 restart

##Set listen address of sshd to lan interface - disabled for now
#source /lib/functions/network.sh
#network_get_ipaddr ip lan
#uci set "sshd.@openssh[0].ListenAddress=$ip"
#uci commit sshd
#/etc/init.d/sshd restart

python /usr/bin/mitm_turris_config.py

/usr/bin/mitmkeygen
/etc/init.d/mitmproxy_wrapper start
/etc/init.d/mitmproxy_wrapper enable
