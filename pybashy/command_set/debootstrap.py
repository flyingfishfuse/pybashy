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
Debian/Ubuntu/Mint/PopOS installation for use as a sandbox
or new OS install.

TODO:
	Download:
		-PopOS Hybrid ISO

	Unpack:
		- PopOS filesystem.squashfs

	Overlay:
		- PopOS filesystem over Ubuntu of same release version

	Mount:
		- /boot/efi 
			add UUID to fstab, mount before chroot
			
	Create:
		- /etc/fstab
		- /etc/resolvconf entries
		- stuff

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
	pass True to "active" to set it to perform the task on init

	'''
	def __init__(self, components,arch,sandy_path,repository, user,password,extras, active = False):
		self.active = active
		self.components = components
		self.arch = arch
		self.sandy_path = sandy_path
		self.repository = repository
		self.user = user
		self.password = password
		self.extras = extras
		#running on init
		if getattr(self, 'active') == True:
			self.do_it_all()


	def do_it_all(self):
		self.debootstrap_action(self.components,self.arch,self.sandy_path,self.repository)
		self.stage1(self.components,self.arch,self.sandy_path,self.repository,self.user,self.password,self.extras)
		self.chroot_staging(self.sandy_path)
		self.stage2(self.sandy_path, self.user, self.password, self.extras)

	def debootstrap_action(self, components,arch,sandy_path,repository):
		steps = {
				 'debootstrap' : ["sudo debootstrap --components {} --arch {} , bionic {} {}".format(components,arch,sandy_path,repository),
				 "[+] Beginning Debootstrap",
				 "[+] Debootstrap Finished Successfully!",
				 "[-]Debootstrap Failed! Check the logfile!"]
				}
		
	def stage1(self, components,arch,sandy_path,repository, user, password, extras):
		'''
	Stage 1 :
		- sets up base files/directory's
			* debootstrap
			* copy resolv.conf
		- mounts for chroot
			* /dev, /proc, /sys
			'''
		# Sequential commands
		steps = {
			'copy_resolvconf':["sudo cp /etc/resolv.conf {}/etc/resolv.conf".format(sandy_path),
			"[+] Copying Resolv.conf",
			"[+] Resolv.conf copied!",
			"[-]Copying Resolv.conf Failed! Check the logfile!"],
			'copy_sourceslist':["sudo cp /etc/apt/sources.list {}/etc/apt/".format(sandy_path)],
			"[+] Copying Sources.list",
			"[+] Sources.list copied!",
			"[-]Copying Sources.list Failed! Check the logfile!"]
			}
		

	def chroot_staging(sandy_path):
		'''
	used in stage2()
		'''
		#mount and bind the proper volumes
		steps = {
				['mount_dev' : "sudo mount -o bind /dev {}/dev".format(sandy_path),"[+] Mounting /dev" "[+] Mounted!", "[-]Mounting /dev Failed! Check the logfile!"],
				['mount_proc' : "sudo mount -o bind -t proc /proc {}/proc".format(sandy_path),"[+] Mounting /proc", "",""],
				['mount_sys' : "sudo mount -o bind -t sys /sys {}/sys".format(sandy_path),"[+] Mounting /sys", "",""]
				}

	def stage2(self, sandy_path, user, password, extras):
		'''
	Establishes Chroot
		- sets username / password

		- LOG'S IN, DONT LEAVE THE COMPUTER
			-for security/data entry purposes

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
 ...
update-initramfs: Generating /boot/initrd.img-5.4.0-7634-generic
kernelstub.Config    : INFO     Looking for configuration...
kernelstub           : WARNING  Live mode is enabled!
Kernelstub is running in live environment mode. This usually means that you are running a live disk, and kernelstub should not run. We are thus exiting with 0.
If you are not running a live disk, please run `sudo kernelstub` to disable live mode.
