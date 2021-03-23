# -*- coding: utf-8 -*-
################################################################################
##            debootstrapy - a linux tool for using debootstrap               ##
################################################################################
# Copyright (c) 2020 Adam Galindo                                             ##
#                                                                             ##
# Permission is hereby granted, free of charge, to any person obtaining a copy##
# of this software and associated documentation files (the "Software"),to deal##
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
This file waaaaaat

"""
__author__     = 'Adam Galindo'
__email__     = 'null@null.com'
__version__ = '1'
__license__ = 'GPLv3'

import os
import inspect
import configparser
from pybashy.CommandRunner import CommandRunner,ExecutionPool,CommandSet
from pybashy.useful_functions import yellow_bold_print,redprint 
from pybashy.useful_functions import parser,list_modules
# TODO: make this file do something to activate the loader with the current environment, keep the setup and init clean
def load_modules_from_config():
    module_pool = {}
    module_loader = CommandRunner()
    if extension in list_modules():
        module_pool[extension] = module_loader.dynamic_import(extension)
    else:
        yellow_bold_print("[-] Module not in framework : " + str(extension))
        raise SystemExit
    # now that the modules are loaded, assign options to kwargs
    kwargs     = {}
    for option, value in config[user_choice]:
        kwargs[option] = value
        thing_to_do = CommandSet()

if __name__ == "__main__":
    import arg_config_parse
    
    def execute_test():
        execution_pool = ExecutionPool()
        command_runner = CommandRunner()
        command_pool   = command_runner.dynamic_import('commandtest')
        # printing the contents

