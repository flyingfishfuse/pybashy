class DnsMasqServer():
    def __init__(self, iface = "eth1"):
        self.dnsmasq_conf_location = '/etc/dnsmasq.conf'
        self.interface     = iface
        self.domain        = "yourdomain.com"
        self.range_bottom  = '192.168.1.11' 
        self.range_top     = '192.168.1.50'
        self.netmask       = '255.255.255.0'
        self.lease_time    = '1h'
        self.dhcp_range    = self.range_bottom + "," + \
                             self.range_top    + "," + \
                             self.netmask      + "," + \
                             self.lease_time
        self.dhcp_boot     = "pxelinux.0,pxeserver"
        self.dhcp_ip       = "192.168.1.4"
        self.pxe_service   = 'x86PC, "Install Linux", pxelinux'
        self.enable_tftp   = 'enable-tftp' 
        self.tftp_root     = '/var/www/tftp'
        self.dnsmasq_start = 'sudo systemctl start dnsmasq.service'
        self.dnsmasq_stop  = 'sudo systemctl stop dnsmasq.service'

        self.dnsmasq_conf = '''
interface={}
domain={}
dhcp-range={}
dhcp-boot={},{}192.168.0.2
pxe-service=x86PC, "Install Linux", pxelinux
enable-tftp
tftp-root=/srv/tftp
'''
        self.dnsmasq_conf.format(self.interface,
                                 self.domain ,
                                 self.dhcp_range ,
                                 self.dhcp_boot ,
                                 self.boot_ip   , 
                                 self.pxe_service ,
                                 self.enable_tftp ,
                                 self.tftp_root 
                                )
        