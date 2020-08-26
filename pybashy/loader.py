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
TODO: build up the execution pool class ya daft loon!
its in commandrunner.py now
	- infrastructure that allows for running bash scripts with python


"""
__author__ 	= 'Adam Galindo'
__email__ 	= 'null@null.com'
__version__ = '1'
__license__ = 'GPLv3'

# the things allowed/expected in a module
basic_items = ['steps','success_message', 'failure_message', 'info_message']
###################################################################################
# Basic imports required for operation
###################################################################################
import os
import sys
import inspect
import argparse
import threading
import configparser

#import the framework
from pybashy.commandrunner import CommandSet
from pybashy.commandrunner import CommandRunner
from pybashy.commandrunner import ExecutionPool
from pybashy.useful_functions import error_message
from pybashy.useful_functions import greenprint,yellow_bold_print,redprint
from pybashy.useful_functions import info_message,warning_message,critical_message
#####################################################################################################################################################################
# Commandline Arguments
###################################################################################
# If the user is running the program as a script we parse the arguments or use the 
# config file. 
# If the user is importing this as a module for usage as a command framework we do
# not activate the argument or configuration file parsing engines
parser = argparse.ArgumentParser(description='python based, bash task execution manager')
parser.add_argument('--testing',
							 dest		= 'testing',
							 action		= "store_true" ,
							 help		= 'will run a series of tests, testing modules not supported yet' )
parser.add_argument('--use-config',
							 dest		= 'config_file',
							 action		= "store_true" ,
							 help		= 'Use config file, if used, will ignore other options' )
parser.add_argument('--config-filename',
							 dest		= 'config_filename',
							 action		= "store" ,
							 help		= 'Name of the config file' )
parser.add_argument('--execute-module',
							 dest		= 'dynamic_import',
							 action		= "store_true" ,
							 help		= 'Will execute user created module if used, will ignore config options ' )
parser.add_argument('--module-name',
							 dest		= 'dynamic_import_name',
							 action		= "store" ,
							 help		= 'Name of module to load' )


if __name__ == "__main__":

	def execute_test():
			#asdf = Stepper()
			#asdf.step_test(asdf.example)
			#asdf.step_test(asdf.example2)
			exec_pool   = ExecutionPool()
			exec_pool(CommandRunner().dynamic_import('commandtest'))
			for command_name,command_set_object in exec_pool.items():
				for thing_name in dir(command_set_object):
					print(command_name)
					if thing_name.startswith('__') != True:
						yellow_bold_print(thing_name)
			
			#finished_task = new_stepper.worker_bee(new_command_set_class,)

	def load_modules():
		module_pool = {}
		module_loader = CommandRunner()
		if extension in module_loader.list_modules():
			module_pool[extension] = module_loader.dynamic_import(extension)
		else:
			yellow_bold_print("[-] Module not in framework : " + str(extension))
			raise SystemExit
			sys.exit()
					# now that the modules are loaded, assign options to kwargs
		kwargs 	= {}
		for option, value in config[user_choice]:
			kwargs[option] = value
		
		#thing_to_do = CommandSet(kwargs)
		#modu


	arguments = parser.parse_args()
	if arguments.testing == True and (arguments.config_file != True):
		execute_test()
	#are we using config?
	if arguments.config_file == True and (arguments.testing != True):
		config = configparser.ConfigParser()
		config.read(arguments.config_path)
		# user needs to set config file or arguments
		user_choice = config['Thing To Do']['choice']
		if user_choice== 'doofus':
			yellow_bold_print("YOU HAVE TO CONFIGURE THE DARN THING FIRST!")
			raise SystemExit
			sys.exit()
		# Doesnt run for choice = DEFAULT unless (look down)
		elif user_choice == 'DEFAULT':
			execute_test()
		#if the user chose a section in the config file
		elif user_choice in config.sections:
			#find the list of modules they want to load
			modules_to_load:list = config['Thing To Do']['modules'].split(',')
			#sort through them to see if they are requesting something that actually exists
			for extension in modules_to_load:
				# make a pool of CommandSet() objects in a dict, named after the module
				load_modules()
		else:
			redprint("[-] Option not in config file")
 	#loading a specialized module
	elif arguments.config_file == False and (arguments.dynamic_import == True):
		new_command = CommandRunner()
		new_command_pool = new_command.dynamic_import(arguments.dynamic_import_name)

