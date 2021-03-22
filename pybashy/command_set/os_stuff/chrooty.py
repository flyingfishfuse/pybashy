
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
     Performs a Chroot operation to enter a sandbox/live_os/target/etc...
"""

__author__ = 'Adam Galindo'
__email__ = 'null@null.com'
__version__ = '1'
__license__ = 'GPLv3'

class Chroot:
    '''
    Does what it says on the label
    '''
    def __init__(self, kwargs):
        for (k, v) in kwargs.items():
            setattr(self, k, v)
    
    def step_on_through(self):
        steps = { 'mount_dev': 
                    ["sudo mount -o bind /dev {}/dev".format(self.chroot_base),
                     "[+] Mounted /dev on {}!".format(self.chroot_base),
                     "[-] Mounting /dev on {} Failed! Check the logfile!".format(self.chroot_base) ],
                 'mount_proc': 
                     ["sudo mount -o bind /proc {}/proc".format(self.chroot_base),
                     "[+] Mounted /proc on {}!".format(self.chroot_base),
                     "[-] Mounting /proc on {} Failed! Check the logfile!".format(self.chroot_base)],
                 'mount_sys': 
                     ["sudo mount -o bind /sys {}/sys".format(self.chroot_base),
                     "[+] Mounted /sys on {}!".format(self.chroot_base),
                     "[-] Mounting /sys on {} Failed! Check the logfile!".format(self.chroot_base)],
                    'move_resolvconf':
                         ["sudo cp /etc/resolv.conf {}/etc/resolv.conf".format(self.chroot_base),
                         "[+] Resolv.conf Copied!",
                         "[-] Failure To Copy Resolv.conf! Check the logfile!"],
                'chroot':    
                    ["sudo chroot {} ".format(chroot_base),
                    "[+] Success!",
                    "[-] Failed! Check the logfile!"]
                }