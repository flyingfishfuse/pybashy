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
debootstrapy:
	- infrastructure that allows for running bash scripts with python
 
	- python based linux tool for using debootstrap to make a networked
		debian based, sandbox OR a live-usb image with persistance
		Using only basic debian/linux/gnu tools

	currently, only a single os live-usb is supported
	
	config file must be named "debootstrapy.config" and be in the same directory

"""
#read, write = os.pipe()
#step = subprocess.Popen(something_to_set_env, 
#						shell=shell_env, 
#						stdin=read, 
#						stdout=sys.stdout, 
#						stderr=subprocess.PIPE)
#Note that this is limited to sending a maximum of 64kB at a time,
# pretty much an interavtice session
#byteswritten = os.write(write, str(command))

import os
import sys
import inspect
import pkgutil
import pathlib
import argparse
import subprocess
import configparser
from pathlib import Path
from io import BytesIO,StringIO
from importlib import import_module

__author__ 	= 'Adam Galindo'
__email__ 	= 'null@null.com'
__version__ = '1'
__license__ = 'GPLv3'

###################################################################################
# Color Print Functions
###################################################################################
import logging 
try:
	import colorama
	from colorama import init
	init()
	from colorama import Fore, Back, Style
	COLORMEQUALIFIED = True
except ImportError as derp:
	print("[-] NO COLOR PRINTING FUNCTIONS AVAILABLE")
	COLORMEQUALIFIED = False

blueprint 			= lambda text: print(Fore.BLUE + ' ' +  text + ' ' + \
	Style.RESET_ALL) if (COLORMEQUALIFIED == True) else print(text)
greenprint 			= lambda text: print(Fore.GREEN + ' ' +  text + ' ' + \
	Style.RESET_ALL) if (COLORMEQUALIFIED == True) else print(text)
redprint 			= lambda text: print(Fore.RED + ' ' +  text + ' ' + \
	Style.RESET_ALL) if (COLORMEQUALIFIED == True) else print(text)
# inline colorization for lambdas in a lambda
makered				= lambda text: Fore.RED + ' ' +  text + ' ' + \
	Style.RESET_ALL if (COLORMEQUALIFIED == True) else None
makegreen  			= lambda text: Fore.GREEN + ' ' +  text + ' ' + \
	Style.RESET_ALL if (COLORMEQUALIFIED == True) else None
makeblue  			= lambda text: Fore.BLUE + ' ' +  text + ' ' + \
	Style.RESET_ALL if (COLORMEQUALIFIED == True) else None
makeyellow 			= lambda text: Fore.YELLOW + ' ' +  text + ' ' + \
	Style.RESET_ALL if (COLORMEQUALIFIED == True) else None
yellow_bold_print 	= lambda text: print(Fore.YELLOW + Style.BRIGHT + \
	' {} '.format(text) + Style.RESET_ALL) if (COLORMEQUALIFIED == True) else print(text)

log_file = '/tmp/logtest'
logging.basicConfig(filename=log_file, format='%(asctime)s %(message)s', filemode='w')
logger		   		= logging.getLogger()
logger.setLevel(logging.DEBUG)

debug_message		= lambda message: logger.debug(blueprint(message)) 
info_message		= lambda message: logger.info(greenprint(message)) 
warning_message 	= lambda message: logger.warning(yellow_bold_print(message)) 
error_message		= lambda message: logger.error(redprint(message)) 
critical_message 	= lambda message: logger.critical(yellow_bold_print(message))
#####################################################################################################################################################################
# Commandline Arguments
###################################################################################
# If the user is running the program as a script we parse the arguments or use the 
# config file. 
# If the user is importing this as a module for usage as a command framework we do
# not activate the argument or configuration file parsing engines

#prevent loading on import
if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='python/bash based, distro repacker')
	parser.add_argument('--use-config',
								 dest		= 'config_file',
								 action		= "store_true" ,
								 help		= 'Use config file, if used, will ignore other options' )
	parser.add_argument('--config-filename',
								 dest		= 'config_filename',
								 action		= "store" ,
								 help		= 'Name of the config file' )
	parser.add_argument('--execute-module',
								 dest		= 'dynamic_import_bool',
								 action		= "store_true" ,
								 help		= 'Will execute user created module if used, will ignore config options ' )
	parser.add_argument('--module-name',
								 dest		= 'dynamic_import_name',
								 action		= "store" ,
								 help		= 'Name of user created module' )

	# dont use this here, not time for it to be parsed yet
	#arguments = parser.parse_args()

class Stepper:
#getattr, setattr and self.__dict__
	'''
Steps through the command list

Load your file of commands and use them like this:

		stepper = Stepper()
		stepper.step(dict_of_commands = steps)
		if isinstance(stepper, Exception):
			error_exit("oh no", stepper)
		else:
			info_message("it did the thing!")
	'''
	def __init__(self):
		self.script_cwd		   	= pathlib.Path().absolute()
		self.script_osdir	   	= pathlib.Path(__file__).parent.absolute()
		self.example  = {"ls_root"  : ["ls -la /", "[+] success message", "[-] failure message" ]}
		self.example2 = {"ls_etc"  : ["ls -la /etc"		  , "[-] failure message", "[+] success message" ] ,
		 	 			 "ls_home" : ["ls -la ~/", "[-] failure message", "[+] success message" ] ,}
	
	def step_test(self, dict_of_commands : dict):
		try:
			for instruction in self.example.values(), self.example2.values():
				cmd 	= instruction[0]
				success = instruction[1]
				fail 	= instruction[2]
				self.current_command = cmd
				stepper = self.exec_command(str(self.current_command))
				if stepper.returncode == 1 :
					info_message(success)
				else:
					error_message(fail)
		except Exception as derp:
			return derp

	def step(self, dict_of_commands : dict):
		try:
			for instruction in dict_of_commands.values():
				cmd 	= instruction[0]
				success = instruction[1]
				fail 	= instruction[2]
				self.current_command = cmd
				stepper = self.exec_command(self.current_command)
				if stepper.returncode == 0 :
					info_message(success)
				else:
					error_message(fail)
		except Exception as derp:
			return derp
	
	def exec_command(self, command, blocking = True, shell_env = True):
		'''TODO: add formatting'''
		try:
			if blocking == True:
				step = subprocess.Popen(command,
										shell=shell_env,
				 						stdout=subprocess.PIPE,
				 						stderr=subprocess.PIPE)
				output, error = step.communicate()
				for output_line in output.decode().split('\n'):
					info_message(output_line)
				for error_lines in error.decode().split('\n'):
					critical_message(error_lines)
				return step
			elif blocking == False:
				# TODO: not implemented yet				
				pass
		except Exception as derp:
			yellow_bold_print("[-] Shell Command failed!")
			return derp

#meta class for loading the command sets into
class CommandSet():
	'''
	Basic structure of the command set execution pool
feed it kwargs
then feed it to the STEPPER
	'''
	def __init__(self, kwargs):
		self.steps = dict
		self.success_message = str
		self.failure_message = str
		#attempt to assign everything
		try:
			for (key, value) in kwargs.items():
				if key in ['steps','success_message', 'failure_message']:
					setattr(self, key, value)
				else:
					raise KeyError(str(key))
		except Exception as derp:
			self.error_exit('[-] CRITICAL ERROR: input file didnt validate, check your syntax maybe?', derp.with_traceback)
		
		self.worker_bee()
		
	def worker_bee(self):
		stepper = Stepper()
		stepper.step(self.steps)
		if isinstance(stepper, Exception):
			stepper.error_exit(self.failure_message, Exception)
		else:
			greenprint(self.success_message)
	
	def error_exit(self, message : str, derp : Exception):
		error_message(message = message)
		print(derp.with_traceback)
		sys.exit()


class CommandRunner:
	'''
NARF!
	'''
	def __init__(self):#,kwargs):
		#for (k, v) in kwargs.items():
		#	setattr(self, k, v)
		pass

	def list_modules(self):
		'''
	Lists modules in command_sets directory
		'''
		list_of_modules = []
		command_files_dir = os.path.dirname(__file__) + "/command_sets"		
		list_of_subfiles  = pkgutil.iter_modules([command_files_dir])
		for x in list_of_subfiles:
			print(x.name)
			list_of_modules.append(x.name)
		return list_of_modules

	###################################################################################
	## Dynamic imports
	###################################################################################
	def dynamic_import(self, module_to_import:str):
		'''
		Dynamically imports a module
			- used for the extensions

		Usage:
			thing = class.dynamic_import('pybash_script.classname', name='fishy')
			returns a CommandSet()
		''' 
		command_files_name = 'command_sets.' + module_to_import
		#command_files_dir = os.path.dirname(__file__) + "/command_sets"
		imported_file		= import_module(command_files_name )#, package='pybashy')
		for thing in dir(imported_file):
			if thing.startswith('__') != True:
				commandset = thing
		
		new_cmds = getattr(imported_file, commandset)
		new_command_set = CommandSet(new_cmds)
		#yellow_bold_print(new_cmds)
		return new_command_set

#loading a module then executing it
if __name__ == "__main__":
	asdf = CommandRunner()
	asdf.dynamic_import('commandtest')
	#arguments = parser.parse_args()
	#if 	arguments.use_args == True:
	#asdf = Stepper()
	#asdf.step_test(asdf.example)
	#asdf.step_test(asdf.example2)
	#qwer = Chroot()
	#qwer.ls_test()

#call via terminal
#if __name__ == "__main__":
#	arguments = parser.parse_args()
	#are we using config?
#	if arguments.config_file == True:
#		config = configparser.ConfigParser()
#		config.read(arguments.config_path)
		# user needs to set config file or arguments
#		user_choice = config['Thing To Do']['choice']
#		if user_choice== 'doofus':
#			yellow_bold_print("YOU HAVE TO CONFIGURE THE DARN THING FIRST!")
#			raise SystemExit
#			sys.exit()
		# Doesnt run for choice = DEFAULT unless (look down)
#		elif user_choice in config.sections or (user_choice == 'DEFAULT'):
#			kwargs = config[user_choice]
#			thing_to_do = CommandRunner(**kwargs)
		
#		else:
#			redprint("[-] Option not in config file")
#	elif arguments.config_file == False and (arguments.dynamic_import == True):
#		new_command = CommandRunner()
#	   new_command_class = new_command.dynamic_import(arguments.dynamic_import, arguments.dynamic_import)
#
#		pass