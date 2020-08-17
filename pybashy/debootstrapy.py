# -*- coding: utf-8 -*-
################################################################################
##			debootstrapy - a linux tool for using debootstrap			      ##
################################################################################
# Copyright (c) 2020 Adam Galindo											  ##
#																			  ##
# Permission is hereby granted, free of charge, to any person obtaining a copy##
# of this software and associated documentation files (the "Software"),to deal##
# in the Software without restriction, including without limitation the rights##
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell   ##
# copies of the Software, and to permit persons to whom the Software is	      ##
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
debootstrapy:
	- infrastructure that allows for running bash scripts with python
 
	- python based linux tool for using debootstrap to make a networked
		debian based, sandbox OR a live-usb image with persistance
		Using only basic debian/linux/gnu tools

	currently, only a single os live-usb is supported
	
	config file must be named "debootstrapy.config" and be in the same directory
	This file is an advanced example, showing how to use everything

"""
import os
import sys
import pathlib
import argparse
import subprocess
import configparser

import pybash

__author__ = 'Adam Galindo'
__email__ = 'null@null.com'
__version__ = '1'
__license__ = 'GPLv3'

###################################################################################
# Commandline Arguments
###################################################################################
# If the user is running the program as a script we parse the arguments or use the 
# config file. 
# If the user is importing this as a module for usage as a command framework we do
# not activate the argument or configuration file parsing engines
if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='python/bash based, distro repacker')
	parser.add_argument('--use-config',
								 dest		= 'config_file',
								 action		= "store_true" ,
								 help		= 'Use config file, if used, will ignore other options' )
	parser.add_argument('--make-disk',
								 dest		= 'make_disk',
								 action		= "store_true" ,
								 help		= 'Makes new partitions and installs Grub2/syslinux, \
									 		   takes device name from fdisk -l. Otherwise, makes a folder' )
	parser.add_argument('--use-iso',
								 dest		= 'use_live_iso',
								 action 	= "store_true" ,
								 help		= 'Uses a Live ISO instead of a repository' )
	parser.add_argument('--iso-name',
								 dest		= 'iso_name',
								 action		= "store" ,
								 help		= 'ISO to use, might need to be in same directory' )
	parser.add_argument('--user',
								 dest	= 'user',
								 action  = "store" ,
								 default = "derp" ,
								 help	= "The username to be created" )
	parser.add_argument('--password',
								 dest	= 'password',
								 action  = "store" ,
								 default = 'password' ,
								 help	= "The password to said username" )
	parser.add_argument('--extra-packages',
								 dest	= 'extra_extra',
								 action  = "store" ,
								 default = 'micro' ,
								 help	= "comma seperated list of extra packages to install" )
	parser.add_argument('--sandbox-hostname',
								 dest	= 'sand_hostname',
								 action  = "store" ,
								 default = 'sandbox' ,
								 help	= "Hostname of the Sandbox" )
	parser.add_argument('--sandbox-mac',
								 dest	= 'sand_mac',
								 action  = "store" ,
								 default = 'de:ad:be:ef:ca:fe' ,
								 help	= "MAC Address of the Sandbox" )
	parser.add_argument('--sandbox-ip',
								 dest	= 'sand_ip',
								 action  = "store" ,
								 default = '192.168.0.3' ,
								 help	= "IP Address of the Sandbox" )							
	parser.add_argument('--sandbox-interface',
								 dest	= 'sand_iface',
								 action  = "store" ,
								 default = 'hack1' ,
								 help	= "Interface name for the Sandbox" )
	parser.add_argument('--sandbox-netmask',
								 dest	= 'sandy_netmask',
								 action  = "store" ,
								 default = '/24' ,
								 help	= 'Netmask for the sandbox in slash notation, e.g. "/24"' )
	parser.add_argument('--sandbox-path',
								 dest	= 'sandy_path',
								 action  = "store" ,
								 default = '/home/moop/Desktop/sandbox' ,
								 help	= "Full Path of the Sandbox" )
	parser.add_argument('--arch',
								 dest	= 'arch',
								 action  = "store" ,
								 default = 'amd64' ,
								 help	= "amd64, x86, arm, ..." )
	parser.add_argument('--components',
								 dest	= 'components',
								 action  = "store" ,
								 default = 'main,contrib,universe,multiverse' ,
								 help	= "Which repository components are included" )
	parser.add_argument('--repository',
								 dest	= 'repository',
								 action  = "store" ,
								 default = "http://archive.ubuntu.com/ubuntu/" ,
								 help	= 'The Debian-based repository. E.g. "Ubuntu"' )		
	parser.add_argument('--livedisk_hw_name',
								 dest	= 'livedisk_hw_name',
								 action  = "store" ,
								 default = "sdc" ,
								 help	= 'Makes new partitions , takes device name from fdisk -l' )
	parser.add_argument('--logfile',
								 dest	= 'log_file',
								 action  = "store" ,
								 default = './debootstrap_log.txt' ,
								 help	= 'logfile name' )
	parser.add_argument('--host-interface',
								 dest	= 'host_iface',
								 action  = "store" ,
								 default = "eth0" ,
								 help	= 'Host network interface to use' )
	parser.add_argument('--internal-ip',
								 dest	= 'internal_ip',
								 action  = "store" ,
								 default = "192.168.0.1" ,
								 help	= 'Host IP address on the chosen interface' )
	parser.add_argument('--network-gateway',
								 dest	= 'gateway',
								 action  = "store" ,
								 default = "192.168.0.1" ,
								 help	= 'Network Gateway IP' )
	# dont use this here, not time for it to be parsed yet
	#arguments = parser.parse_args()

# To make a new program, all you have to do is inherit from CommandRunner
# set whatever you need in __init__ from your arguments or config
class CommandSet():
	'''
	NARF!
	'''
	def __init__(self, kwargs):
		self.extras				= "debconf nano curl"
		self.live_disk_dir		= self.temp_dir + '/live'
		self.temp_boot_dir		= self.live_disk_dir + '/boot'
		self.efi_dir			= self.temp_dir + '/efi'
		self.persistance_dir	= self.temp_dir + '/persistance'
		self.file_source_dir	= self.temp_dir + file_source_dir

#call via terminal
# you must specify either config or arguments
if __name__ == "__main__":
	arguments = parser.parse_args()
	#are we using config?
	if arguments.config_file == True:
		config = configparser.ConfigParser()
		config.read('debootstrapy.config')
		# user needs to set config file or arguments
		user_choice = config['Thing To Do']['choice']
		if user_choice== 'doofus':
			yellow_bold_print("YOU HAVE TO CONFIGURE THE DARN THING FIRST!")
			raise SystemExit
			sys.exit()
		# Doesnt run for choice = DEFAULT unless (look down)
		elif user_choice in config.sections or (user_choice == 'DEFAULT'):
			kwargs = config[user_choice]
			thing_to_do = CommandRunner(**kwargs)
		
		else:
			redprint("[-] Option not in config file")
	elif arguments.config_file == False:
		thing_to_do = CommandRunner(arguments.sand_hostname ,arguments.user	   ,\
					  arguments.password,	arguments.extra_extra	 ,\
					  arguments.sand_mac,	arguments.sand_ip		 ,\
					  arguments.sand_iface, arguments.sandy_netmask ,\
					  arguments.sandy_path, arguments.arch		  ,\
					  arguments.repository, arguments.components	,\
					  arguments.log_file,	arguments.host_iface	  ,\
					  arguments.internal_ip, arguments.gateway	  ,\
					  "debconf nano curl")
		if (arguments.make_disk == True) and (arguments.use_live_iso == True):
			#TODO: should be a path.. or name?
			thing_to_do.file_source = '/tmp/live.iso' # arguments.iso_name
			thing_to_do.setup_disk(diskname="",efi_dir="",persistance_dir="",temp_boot_dir="",live_disk_dir="")
			thing_to_do.move_system_files(efi_dir="",live_disk_dir="",persistance_dir="",file_source_dir="")
			thing_to_do.install_grub2(bit_size="",arch="",livedisk_hw_name="",temp_boot_dir="",efi_dir="")
			#syslinux for USB install
			#thing_to_do.install_syslinux(livedisk_hw_name="",live_disk_dir="",file_source_dir="",efi_dir="",persistance_dir="")

			pass