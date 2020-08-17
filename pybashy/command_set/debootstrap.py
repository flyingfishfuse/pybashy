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

This performs the steps necessary to debootstrap a new
Debian/Ubuntu/Mint installation for use as a sandbox
or new OS install.

"""
import os
import sys

__author__ = 'Adam Galindo'
__email__ = 'null@null.com'
__version__ = '1'
__license__ = 'GPLv3'

class Debootstrap:
	'''
	Does disk stuff
	'''
	def __init__(self, kwargs):
		#for (k, v) in kwargs.items():
		#	setattr(self, k, v)
		pass

	def stage1(self, arch, sandy_path, components, repository):
		'''
	Stage 1 :
		- sets up base files/directory's
			* debootstrap
			* copy resolv.conf
		- mounts for chroot
			* /dev, /proc, /sys
			'''
		# Sequential commands
		"[+] Beginning Debootstrap"
		steps = {[ 'debootstrap_actual' : "sudo debootstrap --components {} --arch {} , bionic {} {}".format(components,arch,sandy_path,repository),
		"[+] Debootstrap Finished Successfully!",
		"[-]Debootstrap Failed! Check the logfile!"]
		}
		#resolv.conf copy
		"[+] Copying Resolv.conf"
		"sudo cp /etc/resolv.conf {}/etc/resolv.conf".format(sandy_path)
		"[+] Resolv.conf copied!"
		"[-]Copying Resolv.conf Failed! Check the logfile!"

		# sources.list copy
		"[+] Copying Sources.list"
		["sudo cp /etc/apt/sources.list {}/etc/apt/".format(sandy_path)]
		"[+] Sources.list copied!"
		"[-]Copying Sources.list Failed! Check the logfile!"

		#mount and bind the proper volumes
		# /dev
		"[+] Mounting /dev" 
		["sudo mount -o bind /dev {}/dev".format(sandy_path)]
		"[+] Mounted!"
		"[-]Mounting /dev Failed! Check the logfile!"
		# /proc
		"[+] Mounting /proc"
		["sudo mount -o bind -t proc /proc {}/proc".format(sandy_path)]
		["sudo mount -o bind -t sys /sys {}/sys".format(sandy_path)]

	def stage2(self, sandy_path, user, password, extras):
		'''
	Establishes Chroot
		- sets username / password

		- LOG'S IN, DONT LEAVE THE COMPUTER
			-for security purposes

		- updates packages
		- installs debconf, nano, curl
		- installs extras

		'''
		steps = {'chroot':
					["sudo chroot {} ".format(sandy_path),
					  "[+] Chrooted!".format(),
					  "[-] Chroot Failed! Check the logfile!".format() 	],
				 'adduser':
					 ["useradd {}".format(user),
					  "[+] User Added!",
					  "[-] Failed! Check the logfile!" 	],
				 'change_password':
					 ["passwd  {}".format(password),
					  "[+] Password Changed!",
					  "[-] Failed! Check the logfile!" 	],
				 'login':
					 ["login {}".format(user),
					  "[+] Logged In!",
					  "[-] Failed! Check the logfile!" 	],
				 'apt_update':
					 ["sudo -S apt-get update",
					  "[+] Packages Updated!",
					  "[-] Failed! Check the logfile!" 	],
				 'apt_install_extras':
					 ["sudo -S apt-get --no-install-recommends install {}".format(extras),
					  "[+] Extras Installed!",
					  "[-] Failed! Check the logfile!" 	]
				}
				# TODO: clean the gpg error message
				# sudo -S apt-get install locales dialog
				# sudo -S locale-gen en_US.UTF-8  # or your preferred locale
				# tzselect; TZ='Continent/Country'; export TZ  #Congure and use our local time instead of UTC; save in .prole
