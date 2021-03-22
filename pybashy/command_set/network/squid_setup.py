
squid_start = 'systemctl start squid.service'
squid_stop = 'systemctl stop squid.service'

squid_conf = '''
acl localnet src 0.0.0.1-0.255.255.255	# RFC 1122 "this" network (LAN)
acl localnet src 10.0.0.0/8		# RFC 1918 local private network (LAN)
acl localnet src 100.64.0.0/10		# RFC 6598 shared address space (CGN)
acl localnet src 192.168.1.0/24		# RFC 1918 local private network (LAN)
                                        # Restricted in size to 255 addresses
acl localnet src fc00::/7       	# RFC 4193 local private network range
acl localnet src fe80::/10      	# RFC 4291 link-local (directly plugged) machines

acl SSL_ports port 443
acl Safe_ports port 80		# http
acl Safe_ports port 21		# ftp
acl Safe_ports port 443		# https
acl Safe_ports port 70		# gopher
acl Safe_ports port 210		# wais
acl Safe_ports port 1025-65535	# unregistered ports
acl Safe_ports port 280		# http-mgmt
acl Safe_ports port 488		# gss-http
acl Safe_ports port 591		# filemaker
acl Safe_ports port 777		# multiling http
acl CONNECT method CONNECT
http_access deny !Safe_ports
http_access deny CONNECT !SSL_ports
http_access allow localhost manager
http_access deny manager
# http_access deny to_localhost
include /etc/squid/conf.d/*
http_access allow localnet
http_access allow localhost
http_access deny all
http_port 3128
coredump_dir /var/spool/squid
refresh_pattern ^ftp:		1440	20%	10080
refresh_pattern ^gopher:	1440	0%	1440
refresh_pattern -i (/cgi-bin/|\?) 0	0%	0
refresh_pattern .		0	20%	4320
'''

squid_chroot = '''
mkdir -p /usr/local/squid3/var/cache/squid3
chown proxy:nogroup /usr/local/squid3/var/cache/squid3
mkdir -p /usr/local/squid3/var/log/squid3
mkdir -p /usr/local/squid3/var/run/nscd
chown proxy:nogroup /usr/local/squid3/var/run
mkdir -p /usr/local/squid3/etc
mkdir -p /usr/local/squid3/lib
mkdir -p /usr/local/squid3/var/spool/squid3
chown proxy:nogroup /usr/local/squid3/var/spool/squid3
mkdir -p /usr/local/squid3/usr/share/squid3
cp /usr/share/squid3/mime.conf /usr/local/squid3/usr/share/squid3/
cp -r /usr/share/squid3/icons /usr/local/squid3/usr/share/squid3/
mkdir -p /usr/local/squid3/etc
cp /etc/resolv.conf /usr/local/squid3/etc/
cp /etc/nsswitch.conf /usr/local/squid3/etc/
mkdir -p /usr/local/squid3/lib
cp /lib/libnss_dns* /usr/local/squid3/lib/
mkdir -p /usr/local/squid3/usr/lib/squid3
cp /usr/lib/squid3/* /usr/local/squid3/usr/lib/squid3/
'''
