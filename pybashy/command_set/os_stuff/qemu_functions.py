
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

"""
# Start a VNC server on display X (accepts an argument (X) for the display 
# number). Substitute X for the number of the display (0 will then listen on 
# 5900, 1 on 5901, etc).
#-display vnc=127.0.0.1:<X>
# Modern chipset (PCIe, AHCI, ...) and hardware virtualization acceleration
# -machine type=q35,accel=kvm
#-device virtio-scsi-pci,id=scsi0 -drive file=/dev/your/block,if=none,
# format=raw,discard=unmap,aio=native,cache=none,id=someid -device scsi-hd,
# drive=someid,bus=scsi0.0
# Pass-through for host random number generator. 
# Accelerates startup of e.g. Debian VMs because of missing entropy.
#-object rng-random,id=rng0,filename=/dev/urandom -device virtio-rng-pci,rng=rng0
class QemuBoxen():
    def __init__(self,kwargs):
        self.machine_type = "q35"
        self.accel = ["kvm"]
        self.use_kvm = True
        self.cpu_type = ["base", "max", "host","qemu32",
            "qemu64","kvm64","kvm32","EPYC",
            "486","IvyBridge","SandyBridge",
            "phenom"]
        self.num_cores          = ["2","4","8"]
        self.options_list       = ["-display","-machine", "-smp","-cpu","-m", "-drive",
                                   "-cdrom","-vga","-netdev","-smb","-usbdevice","-k","-snapshot"]
        self.display_options    = ["sdl","curses","gtk","vnc"]
        self.vga_options        = ["cirrus","std","vmware","qxl"]
        self.network_options    = ["id","mac","net","ipv4","ipv6","host","ipv6-net","ipv6-host",
                                    "restrict","hostname","dhcpstart","dns","ipv6-dns",
                                    "dnssearch","domainname","tftp","tftp-server-name","bootfile",
                                    "smb","hostfwd","guestfwd","","",""]
        self.drive_options      = ["file","cache","format","id","media",""]
        self.arg_array          = []
        self.final_arg_string   = ""

        for option,argument in qemu_boot_options:
            # validate thing
            if option in self.options_list.strip("-"):
                self.arg_array.append(option + " " + argument)
            setattr(self, option, argument)

    def qemu_setup_qcow(new_image_name, new_image_size):
    # one type hdd
        steps = {   'qemu_create_qcow' : ["qemu-img create -f qcow2 {} {}".format(new_image_name, new_image_size),
                        'success_message'    : "[+]     Sucessful!",
                        'failure_message'     : "[-]     Failure!"]
                }
        info_message    = "[+] Informational Text!"
        success_message = "[+] Test Sucessful!"
        failure_message = "[-] Test Failure!"
                    # start with interface set
                    #ifname=tap0 - the tap name here corresponds with the name in the bridge stanza above.
                    #script=no,downscript=no disable the scripts /etc/qemu-ifup and /etc/qemu-ifdown as they are not needed.

    def qemu_boot_image(qemu_boot_options):
        steps = {   'qemu_boot' : ["qemu-system-x86_64 {}".format(qemu_boot_options),
                    'success_message'    : "[+]     Sucessful!",
                    'failure_message'     : "[-]     Failure!"]

                }
        info_message    = "[+] Informational Text!"
        success_message = "[+] Test Sucessful!"
        failure_message = "[-] Test Failure!"