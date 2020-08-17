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

it will take a dict from a file and assign it a CommandSet class
with the key assigned to attribute
"""

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

__author__ = 'Adam Galindo'
__email__ = 'null@null.com'
__version__ = '1'
__license__ = 'GPLv3'
#__module__ = 'pybash'
###################################################################################
# Color Print/logging Functions
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
##################################################################################
##################################################################################
class Stepper:
#getattr, setattr and self.__dict__
	'''
Steps through the command list
	'''
	def __init__(self):
		self.script_cwd		   	= pathlib.Path().absolute()
		self.script_osdir	   	= pathlib.Path(__file__).parent.absolute()
		self.example  = {"ls_root"  : ["ls -la /", "[+] success message", "[-] failure message" ]}
		self.example2 = {"ls_etc"  : ["ls -la /etc"		  , "[-] failure message", "[+] success message" ] ,
		 	 			 "ls_home" : ["ls -la ~/", "[-] failure message", "[+] success message" ] ,}

	def error_exit(self, message : str, derp : Exception):
		error_message(message = message)
		print(derp.with_traceback)
		sys.exit()
	
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
feed it kwargs

	'''
	def __init__(self, kwargs):
		pass

class CommandRunner:
	'''
NARF!
	'''
	def __init__(self):
		#for (k, v) in kwargs.items():
		#	setattr(self, k, v)
		# do stuff here?
		print("[+] Command Framework Loaded")

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
		''' 
		# make a filter
		class_filter = ["asdf"]
		classname = lambda classname: classname != any(class_filter) and not classname.startswith('__')
		# folder we shove the files in
		command_files_name = '.command_sets.'
		command_files_dir = os.path.dirname(__file__) + "/command_sets"
		#import the module
		#package must be the name of this package for relative import
		imported_file		= import_module((command_files_name + module_to_import), package='pybash')
		yellow_bold_print(dir(imported_file))
		print(filter(classname(), dir(imported_file)))
		#
		class_name			= list(filter(classname(), dir(imported_file)))
		# gets the 
		new_class			= getattr(imported_module, class_name[0])
		print(new_class)

		#json_acceptable_string = s.replace("'", "\"")
		#d = json.loads(json_acceptable_string)
		#steps = jsonpickle.decode(new_class)
		print(steps)
		# need to put an error check here
		#make a CommandSet() meta class
		new_command_set = CommandSet()

		# grab all command_sets from imported module
		# assign them as class attributes to CommandSet() Class
		#if isinstance(dict_of_commands, dict):
		#	setattr(, name, value)
		print(sys.modules[__name__])
		setattr(sys.modules[__name__], name, new_class)

		return new_class

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