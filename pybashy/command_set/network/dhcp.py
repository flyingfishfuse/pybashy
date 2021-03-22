# isc_dhcp_server

# necessary for debian
# put one in the other
INTERFACES       = "eth0"
server_conf_file = '/etc/default/isc-dhcp-server'

subnet            = '192.168.1.0'
netmask           = '255.255.255.0'
range_bottom      = '192.168.1.11'
range_top         = '192.168.1.55'
router_ip         = '192.168.1.1'
broadcast_address = '192.168.1.255'


dhcpd_conf = '''
option domain-name "dev.net";
option domain-name-servers ns1.example.org, ns2.example.org;
default-lease-time 600;
max-lease-time 7200;
ddns-update-style none;
authoritative;
subnet {} netmask {} {
  range {} {};
  option broadcast-address {};
  option routers {};             # our router
  option domain-name-servers {}; # our router, again
}
'''.format(subnet,
           netmask,
           range_bottom,
           range_top,
           broadcast_address,
           router_ip,
           dns_server
           )

pxe_boot_conf = '''
default-lease-time 600;
max-lease-time 7200;

allow booting;

# in this example, we serve DHCP requests from 192.168.0.(3 to 253)
# and we have a router at 192.168.0.1
subnet {} netmask {} {
  range {} {};
  option broadcast-address {};
  option routers {};             # our router
  option domain-name-servers {}; # our router, again
  filename "{}"; # (this we will provide later)
}
'''.format(subnet,
           netmask,
           range_bottom,
           range_top,
           broadcast_address,
           router_ip,
           dns_server,
           filename_pxe
           )