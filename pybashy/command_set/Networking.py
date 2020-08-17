
# -*- coding: utf-8 -*-
################################################################################
##			debootstrapy - a linux tool for using debootstrap				  ##
################################################################################
# Copyright (c) 2020 Adam Galindo											  ##
#																			  ##
# Permission is hereby granted, free of charge, to any person obtaining a copy##
# of this software and associated documentation files (the "Software"),to deal##
# in the Software without restriction, including without limitation the rights##
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell   ##
# copies of the Software, and to permit persons to whom the Software is		  ##
# furnished to do so, subject to the following conditions:					  ##
#																			  ##
# Licenced under GPLv3														  ##
# https://www.gnu.org/licenses/gpl-3.0.en.html								  ##
#																			  ##
# The above copyright notice and this permission notice shall be included in  ##
# all copies or substantial portions of the Software.						  ##
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
This is a test of the command framework

It will do the debootstrap stuff

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
deboot_third_stage = ["sudo -S apt install {}".format(extra_packages)]
#Makes an interface with iproute1
create_iface_ipr1 = ["sudo -S modprobe dummy",
					 "sudo -S ip link set {} dev dummy0".format(sandy_iface),
					 "sudo -S ifconfig {} hw ether {}".format(sandy_iface, sandy_mac)
					 ]
#Makes an interface with iproute2
create_iface_ipr2 = ["ip link add {} type veth".format(sandy_iface)]
del_iface1 = ["sudo -S ip addr del {} brd + dev {}".format(sandy_ip,sandy_netmask,sandy_iface),
				 "sudo -S ip link delete {} type dummy".format(sandy_iface),
				 "sudo -S rmmod dummy".format()]
#Deletes the SANDBOX Interface
del_iface2 = ["ip link del {}".format(sandy_iface)]
#run this from the HOST
#Allow forwarding on HOST IFACE
establish_network_forwarding = ["sysctl -w net.ipv4.conf.{}.forwarding=1".format(host_iface),
#Allow from sandbox to outside
	 "iptables -A FORWARD -i {} -o {} -j ACCEPT".format(sandy_iface, host_iface),
#Allow from outside to sandbox
	 "iptables -A FORWARD -i {} -o {} -j ACCEPT".format(host_iface, sandy_iface)]
#run this from the Host
# 1. Delete all existing rules
establish_iptables = {'iptables_FLUSH': ["iptables -F" , " Successful!"," Failed!"],
	# 2. Set default chain policies
			 'iptables_DROP_INPUT': ["iptables -P INPUT DROP", " Successful!"," Failed!"],
			 'iptables_DROP_FORWARD': ["iptables -P FORWARD DROP", " Successful!"," Failed!"],
			 'iptables_DROP_OUTPUT': ["iptables -P OUTPUT DROP", " Successful!"," Failed!"],
			#4. Allow ALL incoming SSH
			'allow_ssh_in': ["iptables -A INPUT -i eth0 -p tcp --dport 22 -m state --state NEW,ESTABLISHED -j ACCEPT", " Successful!"," Failed!"],
			'allow_ssh_out': ["iptables -A OUTPUT -o eth0 -p tcp --sport 22 -m state --state ESTABLISHED -j ACCEPT", " Successful!"," Failed!"],
			# Allow incoming HTTPS
			'allow_https_in': ["iptables -A INPUT -i eth0 -p tcp --dport 443 -m state --state NEW,ESTABLISHED -j ACCEPT", " Successful!"," Failed!"],
			'allow_https_out': ["iptables -A OUTPUT -o eth0 -p tcp --sport 443 -m state --state ESTABLISHED -j ACCEPT", " Successful!"," Failed!"],
			# 19. Allow MySQL connection only from a specic network
			'allow_mysql_specific1': ["iptables -A INPUT -i eth0 -p tcp -s 192.168.200.0/24 --dport 3306 -m state --state NEW,ESTABLISHED -j ACCEPT", " Successful!"," Failed!"],
			'allow_mysql_specific2': ["iptables -A OUTPUT -o eth0 -p tcp --sport 3306 -m state --state ESTABLISHED -j ACCEPT", " Successful!"," Failed!"],
			'prevent_dos': ["iptables -A INPUT -p tcp --dport 80 -m limit --limit 25/minute --limit-burst 100 -j ACCEPT", " Successful!"," Failed!"]
				}
