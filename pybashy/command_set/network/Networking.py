
# -*- coding: utf-8 -*-
################################################################################
##            debootstrapy - a linux tool for using debootstrap                  ##
################################################################################
# Copyright (c) 2020 Adam Galindo                                              ##
#                                                                              ##
# Permission is hereby granted, free of charge, to any person obtaining a copy##
# of this software and associated documentation files (the "Software"),to deal##
# in the Software without restriction, including without limitation the rights##
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell   ##
# copies of the Software, and to permit persons to whom the Software is          ##
# furnished to do so, subject to the following conditions:                      ##
#                                                                              ##
# Licenced under GPLv3                                                          ##
# https://www.gnu.org/licenses/gpl-3.0.en.html                                  ##
#                                                                              ##
# The above copyright notice and this permission notice shall be included in  ##
# all copies or substantial portions of the Software.                          ##
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
####
################################################################################

"""
It will perform networking functions
"""
import os
import sys
import pathlib
import subprocess
from pathlib import Path

__author__ = 'Adam Galindo'
__email__ = 'null@null.com'
__version__ = '1'
__license__ = 'GPLv3'

# begin setting up services
# Installs extra user packages
apt_install = { 'apt_install'     : ["sudo -S apt install {}".format(packages), 
                    'info_message'        : "[+] Informational Text!",
                    'success_message'    : "[+]     Sucessful!",
                    'failure_message'    : "[-]     Failure!"]
                }

def auto_iface_manual():
    payload = '''
#auto eth0
iface eth0 inet manual
'''

def interface_prototype():
    payload = '''
auto br0
iface br0 inet dhcp
pre-up ip tuntap add dev tap0 mode tap user <username>
pre-up ip link set tap0 up
bridge_ports all tap0
bridge_stp off
bridge_maxwait 0
bridge_fd      0
post-down ip link set tap0 down
post-down ip tuntap del dev tap0 mode tap
'''

#Makes an interface with iproute1
create_dummy_interface1 = { 'modprobe_dummy'        : ["sudo -S modprobe dummy",
                                'info_message'        : "[+] Informational Text!",
                                'success_message'    : "[+]     Sucessful!",
                                'failure_message'     : "[-]     Failure!"],
                             'set_dummy_device'     : ["sudo -S ip link set {} dev dummy0".format(sandy_iface),
                                 'info_message'        : "[+] Informational Text!",
                                'success_message'     : "[+]     Sucessful!",
                                'failure_message'     : "[-]     Failure!"],
                             'give_dummy_mac'        : ["sudo -S ifconfig {} hw ether {}".format(sandy_iface, sandy_mac),
                                 'info_message'        : "[+] Informational Text!",
                                'success_message'     : "[+]     Sucessful!",
                                'failure_message'     : "[-]     Failure!"]
                            }        
#Makes an interface with iproute2
create_dummy_interface1 = { 'create_dummy_interface' : ["ip link add {} type veth".format(sandy_iface)],
                                'info_message'      : "[+] Informational Text!",
                                'success_message' : "[+]     Sucessful!",
                                'failure_message' : "[-]     Failure!"]
                            }

remove_dummy_interface = { 'remove_dummy_device' : ["sudo -S ip addr del {} brd + dev {}".format(sandy_ip,sandy_netmask,sandy_iface)],
                                'info_message'        : "[+] Informational Text!",
                                'success_message'    : "[+]     Sucessful!",
                                'failure_message'    : "[-]     Failure!"],
                      'delete_dummy_interface'   : [ "sudo -S ip link delete {} type dummy".format(sandy_iface)],
                                'info_message'        : "[+] Informational Text!",
                                'success_message'    : "[+]     Sucessful!",
                                'failure_message'    : "[-]     Failure!"],
                      'remove_dummy_module    '      : [ "sudo -S rmmod dummy".format(),
                                'info_message'        : "[+] Informational Text!",
                                'success_message'    : "[+]     Sucessful!",
                                'failure_message'    : "[-]     Failure!"]

            }
#Deletes the SANDBOX Interface
del_iface2 = { '' : ["ip link del {}".format(sandy_iface), " Successful!"," Failed!"],
#run this from the HOST
#Allow forwarding on HOST IFACE
set_network_forwarding = {     '' : ["sysctl -w net.ipv4.conf.{}.forwarding=1".format(host_iface),
                                'info_message'        : "[+] Informational Text!",
                                'success_message'    : "[+]     Sucessful!",
                                'failure_message'    : "[-]     Failure!"],
                            #Allow from sandbox to outside
                            '' : ["iptables -A FORWARD -i {} -o {} -j ACCEPT".format(sandy_iface, host_iface),
                                'info_message'        : "[+] Informational Text!",
                                'success_message'    : "[+]     Sucessful!",
                                'failure_message'    : "[-]     Failure!"],
                            #Allow from outside to sandbox
                             '' : ["iptables -A FORWARD -i {} -o {} -j ACCEPT".format(host_iface, sandy_iface),
                                'info_message'        : "[+] Informational Text!",
                                'success_message'    : "[+]     Sucessful!",
                                'failure_message'    : "[-]     Failure!"]
                        }
#run this from the Host
# 1. Delete all existing rules
establish_iptables = { 'iptables_FLUSH': ["iptables -F" ,
                        'info_message'        : "[+] Informational Text!",
                        'success_message'    : "[+]     Sucessful!",
                        'failure_message'    : "[-]     Failure!"]

    # 2. Set default chain policies
             'iptables_DROP_INPUT': ["iptables -P INPUT DROP",
                        'info_message'        : "[+] Informational Text!",
                        'success_message'    : "[+]     Sucessful!",
                        'failure_message'    : "[-]     Failure!"]
             'iptables_DROP_FORWARD': ["iptables -P FORWARD DROP",
                        'info_message'        : "[+] Informational Text!",
                        'success_message'    : "[+]     Sucessful!",
                        'failure_message'    : "[-]     Failure!"]
             'iptables_DROP_OUTPUT': ["iptables -P OUTPUT DROP",
                        'info_message'        : "[+] Informational Text!",
                        'success_message'    : "[+]     Sucessful!",
                        'failure_message'    : "[-]     Failure!"]
            #4. Allow ALL incoming SSH
            'allow_ssh_in': ["iptables -A INPUT -i eth0 -p tcp --dport 22 -m state --state NEW,ESTABLISHED -j ACCEPT",
                        'info_message'        : "[+] Informational Text!",
                        'success_message'    : "[+]     Sucessful!",
                        'failure_message'    : "[-]     Failure!"]
            'allow_ssh_out': ["iptables -A OUTPUT -o eth0 -p tcp --sport 22 -m state --state ESTABLISHED -j ACCEPT",
                        'info_message'        : "[+] Informational Text!",
                        'success_message'    : "[+]     Sucessful!",
                        'failure_message'    : "[-]     Failure!"]
            # Allow incoming HTTPS
            'allow_https_in': ["iptables -A INPUT -i eth0 -p tcp --dport 443 -m state --state NEW,ESTABLISHED -j ACCEPT",
                        'info_message'        : "[+] Informational Text!",
                        'success_message'    : "[+]     Sucessful!",
                        'failure_message'    : "[-]     Failure!"]
            'allow_https_out': ["iptables -A OUTPUT -o eth0 -p tcp --sport 443 -m state --state ESTABLISHED -j ACCEPT",
                        'info_message'        : "[+] Informational Text!",
                        'success_message'    : "[+]     Sucessful!",
                        'failure_message'    : "[-]     Failure!"]
            # 19. Allow MySQL connection only from a specic network
            'allow_mysql_specific1': ["iptables -A INPUT -i eth0 -p tcp -s 192.168.200.0/24 --dport 3306 -m state --state NEW,ESTABLISHED -j ACCEPT",
                        'info_message'        : "[+] Informational Text!",
                        'success_message'    : "[+]     Sucessful!",
                        'failure_message'    : "[-]     Failure!"]
            'allow_mysql_specific2': ["iptables -A OUTPUT -o eth0 -p tcp --sport 3306 -m state --state ESTABLISHED -j ACCEPT",
                        'info_message'        : "[+] Informational Text!",
                        'success_message'    : "[+]     Sucessful!",
                        'failure_message'    : "[-]     Failure!"]
            'prevent_dos': ["iptables -A INPUT -p tcp --dport 80 -m limit --limit 25/minute --limit-burst 100 -j ACCEPT",
                        'info_message'        : "[+] Informational Text!",
                        'success_message'    : "[+]     Sucessful!",
                        'failure_message'    : "[-]     Failure!"]
                }
