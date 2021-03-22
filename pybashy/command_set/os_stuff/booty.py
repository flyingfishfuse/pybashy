# -*- coding: utf-8 -*-
################################################################################
##			debootstrapy - a linux tool for using chroot					  ##
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
This is a more advanced example of the command framework
 - you can use code inside the function to modify information
	before applying the script

This file will do some disk operations necessary for usb live installs

"""
__author__ = 'Adam Galindo'
__email__ = 'null@null.com'
__version__ = '1'
__license__ = 'GPLv3'

def function_install_grub2(self, bit_size, arch, livedisk_hw_name, temp_boot_dir , efi_dir):
	'''
	 Install GRUB2
	 https://en.wikipedia.org/wiki/GNU_GRUB
	 Script supported targets: arm64-efi, x86_64-efi, , i386-efi
	TODO : Install 32bit brub2 then 64bit brub2 then `update-grub`
		   So's we can install 32 bit OS to live disk.
	'''
	#########################
	##	  64-BIT OS	   #
	#########################
	bit_sizey = lambda bit_size: True if bit_size in ("32","64") else False
	archy = {'arm'   : 'arm-efi'  ,\
			 'x86'   : 'i386-efi' ,\
			 'amd64' : 'X86-64-efi'
			}
	if bit_sizey(bit_size) and (archy.get(arch) != 'arm'):
	 	architecture = archy.get(arch)
	elif archy.get(arch) == 'arm':
	 	architecture = arch

	steps = 'grub-install --removable --target={} --boot-directory={} --efi-directory={} /dev{}'.format(\
				architecture,\
				temp_boot_dir,\
				efi_dir,\
				livedisk_hwname)

	info_message	= "[+] Installing GRUB2 for {} to /dev/{}".format(architecture, livedisk_hw_name)
	success_message = "[+] GRUB2 Install Finished Successfully!"
	failure_message = "[-]GRUB2 Install Failed! Check the logfile!"
	
def function_install_syslinux_liveusb(self, livedisk_hw_name, live_disk_dir, file_source_dir, efi_dir, persistance_dir, ):
	# Copy the MBR for syslinux booting of LIVE disk 
	steps = { 'dd_syslinux':
				  ["dd bs=440 count=1 conv=notrunc if=/usr/lib/syslinux/mbr/gptmbr.bin of=/dev/{}".format(livedisk_hw_name) ,
					"",	""],
					# Install Syslinux
					# https://wiki.syslinux.org/wiki/index.php?title=HowTos
				 'syslinux_install ':
					["syslinux --install /dev/{}2".format(livedisk_hw_name) ,
					"",	""],
				 'rename_isolinux_syslinux ':
					["mv {}/isolinux {}/syslinux".format(live_disk_dir ,live_disk_dir) ,
					"",	""],
				 'move_isolinuxbin_syslinuxbin':
					["mv {}/syslinux/isolinux.bin {}/syslinux/syslinux.bin".format(live_disk_dir ,live_disk_dir ) ,
					"",	""],
				 'move_isocfg_syscfg':
					["mv {}/syslinux/isolinux.cfg {}/syslinux/syslinux.cfg".format(live_disk_dir ,live_disk_dir ) ,
					"",	""],
				 'sed_edit1':
					# Magic, sets up syslinux configuration and layouts 
					["sed --in-place 's#isolinux/splash#syslinux/splash#' {}/boot/grub/grub.cfg".format(live_disk_dir) ,
					"",	""],
				 'sed_edit2':
					["sed --in-place '0,/boot=live/{s/\(boot=live .*\)$/\1 persistence/}' {}/boot/grub/grub.cfg {}/syslinux/menu.cfg".format(live_disk_dir , live_disk_dir ) ,
					"",	""],
				 'sed_edit3':
					["sed --in-place '0,/boot=live/{s/\(boot=live .*\)$/\1 keyboard-layouts=en locales=en_US/}' {}/boot/grub/grub.cfg {}/syslinux/menu.cfg".format(live_disk_dir, live_disk_dir  ) ,
					"",	""],
				 'sed_edit4':
					["sed --in-place 's#isolinux/splash#syslinux/splash#' {}/boot/grub/grub.cfg".format(live_disk_dir ),
					"",	""],
				# Clean up!
				 'cleanup1':
					 ["umount {} {} {} {}".format(efi_dir, live_disk_dir ,persistance_dir, file_source_dir) ,
					"",""] ,
				 'cleanup2': 
					 ["rmdir {} {} {} {}".format(efi_dir, live_disk_dir ,persistance_dir, file_source_dir) , 
					"",""]
				}
	info_message	= "[+] Installing Syslinux"
	success_message = "[+] Syslinux Installed!"
	failure_message = "[-]Syslinux Install Failed! Check the logfile!"


