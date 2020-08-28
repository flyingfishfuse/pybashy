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
This file contains the program options 

"""
__author__     = 'Adam Galindo'
__email__     = 'null@null.com'
__version__ = '1'
__license__ = 'GPLv3'

import argparse
import configparser

####################################################################################
# Commandline Arguments
###################################################################################
# If the user is running the program as a script we parse the arguments or use the 
# config file. 
# If the user is importing this as a module for usage as a command framework we do
# not activate the argument or configuration file parsing engines
parser = argparse.ArgumentParser(description='python based, bash task execution manager')

parser.add_argument('--testing',
                             dest    = 'testing',
                             action  = "store_true" ,
                             help    = 'will run a series of tests, testing modules not supported yet' )
parser.add_argument('--use-config',
                             dest    = 'config_file',
                             action  = "store_true" ,
                             help    = 'Use config file, if used, will ignore other options' )
parser.add_argument('--config-filename',
                             dest    = 'config_filename',
                             action  = "store" ,
                             help    = 'Name of the config file' )
parser.add_argument('--execute-module',
                             dest    = 'dynamic_import',
                             action  = "store_true" ,
                             help    = 'Will execute user created module if used, will ignore config options ' )
parser.add_argument('--module-name',
                             dest    = 'dynamic_import_name',
                             action  = "store" ,
                             help    = 'Name of module to load' )

# TODO: make this file do something to activate the loader with the current environment, keep the setup and init clean

if __name__ == "__main__":
    arguments = parser.parse_args()
