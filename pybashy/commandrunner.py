# -*- coding: utf-8 -*-
################################################################################
##                         pybashy - commandrunner.py                         ##
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
#                                                                             ##
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR  ##
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,    ##
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE ##
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER      ##
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,#
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN   ##
# THE SOFTWARE.                                                               ##
################################################################################
"""
TODO: build up the execution pool class ya daft loon!
    - infrastructure that allows for running bash scripts with python


"""
__author__ 	= 'Adam Galindo'
__email__ 	= 'null@null.com'
__version__ = '1'
__license__ = 'GPLv3'

import os
import sys
import pkgutil
import threading
import subprocess
from pathlib import Path
from importlib import import_module
from pybashy.useful_functions import greenprint,yellow_bold_print,redprint
from pybashy.useful_functions import info_message,warning_message,critical_message
from pybashy.useful_functions import error_message

basic_items = ['steps','success_message', 'failure_message', 'info_message']

###############################################################################
###############################################################################
class Command:
	'''
	This class hold each individual step
	It is the direct translation of :
		{'test1' : ['ls -la ~/','','','']}

	'''
	def __init__(self,command: dict):
		self.command = command
		self.cmd_line = str
		self.info_message = str
		self.success_message = str
		self.failure_message = str
		self.name = str

		for key,value in self.command.items():
			setattr(self, key, value)
			self.__name__ = key
	
	def __repr__():
		print(self.__name__)

	def __name__(self):
		return self.name



###############################################################################
###############################################################################
class ExecutionPool():
	'''
	This is the command pool threading class, a container I guess?
	I dunno, I change things fast and loose
	'''
	def __init__(self):
		pool = {'test_init': Command({'test1' : ['ls -la ~/','info','pass','fail']})}
		self.script_cwd		   	= Path().absolute()
		self.script_osdir	   	= Path(__file__).parent.absolute()
		self.example  = {"ls_root" : ["ls -la /", "info", "[+] success message", "[-] failure message" ]}
		self.example2 = {"ls_etc"  : ["ls -la /etc"	,'info', "[-] failure message", "[+] success message" ] ,
		 	 			 "ls_home" : ["ls -la ~/", 'info', "[-] failure message", "[+] success message" ]}


	def error_exit(self, message : str, derp : Exception):
		error_message(message = message)
		print(derp.with_traceback)
		sys.exit()	

	def step(self, dict_of_commands : dict):
		try:
			for instruction in dict_of_commands.values():
				cmd 	= instruction[0]
				info    = instruction[1]
				success = instruction[2]
				fail 	= instruction[3]
				yellow_bold_print(info)
				self.current_command = cmd
				cmd_exec = self.exec_command(self.current_command)
				if cmd_exec.returncode == 0 :
					info_message(success)
				else:
					error_message(fail)
		except Exception as derp:
			return derp
	
	def worker_bee(self, flower , pollen = ''):
		'''
	Worker_bee() gathers up all the things to do and brings them to the stepper
	Dont run this function unless you want to run the scripts!
	
		- Flower is a CommandSet() and is Required
		
		- Pollen is the name of the function to run!
			only required if running in scripting mode
		'''
		try:
			#requesting a specific function_function
			if pollen != '':
				#filter out class stuff, we are searching for functions
				for thing in dir(flower):
					if thing.startswith('function') and thing.endswith(pollen):
						self.success_message = getattr(thing,'success_message')
						self.failure_message = getattr(thing,'failure_message')
						self.info_message	 = getattr(thing,'info_message')
						self.steps			 = getattr(thing,'steps')
						stepper = self.step(self.steps)
						if isinstance(stepper, Exception):
							self.error_exit(self.failure_message, Exception)
						else:
							print(self.success_message)
			# the user wants to run all functions in the class
			else:
				for thing in dir(flower):
					if thing.startswith('__') != True:
						#if we imported a function, assign things properly
						if thing.startswith('function'):
							print(thing)
							self.success_message = getattr(thing,'success_message')
							self.failure_message = getattr(thing,'failure_message')
							self.info_message	 = getattr(thing,'info_message')
							self.steps			 = getattr(thing,'steps')
							stepper = self.step(self.steps)
							if isinstance(stepper, Exception):
								self.error_exit(self.failure_message, Exception)
							else:
								print(self.success_message)
			# otherwise, everything is already assigned
			stepper = self.step(self.steps)
			if isinstance(stepper, Exception):
				print(stepper.error_message)
				raise stepper
			else:
				print(stepper.success_message)
		except Exception as derp:
			self.error_exit(self.failure_message, derp)

	def exec_command(self, command, blocking = True, shell_env = True):
		'''TODO: add formatting'''
		#read, write = os.pipe()
#		step = subprocess.Popen(something_to_set_env, 
#						shell=shell_env, 
#						stdin=read, 
#						stdout=sys.stdout, 
#						stderr=subprocess.PIPE)
#		Note that this is limited to sending a maximum of 64kB at a time,
# 		pretty much an interactive session
#		byteswritten = os.write(write, str(command))

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
	
	def threader(self, thread_function, name):
		info_message("Thread {}: starting".format(name))
		thread = threading.Thread(target=thread_function, args=(1,))
		thread.start()
		info_message("Thread {}: finishing".format(name))

	def add_attributes_kwargs(self, kwargs):
		for (k, v) in kwargs.items():
			setattr(self, k, v)
	
	def new_command_set(self, command_set: CommandSet):
		pass


###############################################################################
###############################################################################
class CommandSet():
	'''
	Basic structure of the command set execution pool
	This is essentially the file/module loaded into a Class
		- All the stuff at the top level of the scope 
			- defs as thier name
			- variables as thier name
			- everything is considered an individual command 
			  unless it matches a keyword like "steps"
				- Those commands are turned into Command() 's 
	
		- feed it kwargs
	
		- put it in the execution pool
	
		- then feed it to the STEPPER
	'''
	#def __new__(cls, clsname, bases, clsdict):
	#	return super().__new__(cls, clsname, bases, clsdict)
	def __init__(self): #, kwargs):
		self.steps   	  = dict
		#self.command_list = []
		#if key in basic_items or (key.startswith('function')):
		self.command_list = {}

	def run_command(self, command):
		for key, value in self.steps.items():
			if key == command:
				print(key,value)
				Command(command)

	def split_to_commands(self, kwargs):
		''' 
		feed it a "steps" variable and it will split it to Command()

		'''
		for key, value in list(stuff.items()):
			Command(command)

	def error_exit(self, message : str, derp):
		#error_message(message = message)
		print(derp.with_traceback)
		#sys.exit()	
	
	def add_command(self, kwargs):
		'''
This is a future method to add commands from the terminal
		'''
		self.command_list.append(Command(**kwargs))

###############################################################################
###############################################################################

class CommandRunner:
	'''
NARF!
Goes running after commands
	'''
	def __init__(self):#,kwargs):
		#for (k, v) in kwargs.items():
		#	setattr(self, k, v)
		pass

	def list_modules(self):
		'''
	Lists modules in command_set directory
		'''
		list_of_modules = []
		command_files_dir = os.path.dirname(__file__) + "/commandset"		
		list_of_subfiles  = pkgutil.iter_modules([command_files_dir])
		for filez in list_of_subfiles:
			print(filez.name)
			list_of_modules.append(filez.name)
		return list_of_modules

	def get_stuff(self, file_import):
		# we are differentiating between functions and other stuff
		# because we want to expand later
		kwargs 				= {}
		kwargs_functions 	= {}
		command_pool        = {}
		#basic_items = ['steps','success_message', 'failure_message', 'info_message']
		try:
			for thing_name in dir(file_import):
				# we are filtering out internal stuff
				# only draw from that when necessary
				if thing_name.startswith('__') != True:
					#grabbing the functions steps
					# remember, everything has been preprocessed by the python
					# interpreter and all we have are "steps" and messages now
					if thing_name.startswith('function'):
						new_command_set = CommandSet()
						#kwargs_functions[thing_name]           = getattr(file_import, thing_name)
						kwargs_functions['__name__']           = getattr(file_import, thing_name)
						kwargs_functions['steps']              = getattr(thing_name,'steps')
						kwargs_functions['info_message']       = getattr(file_import, 'info_message')
						kwargs_functions['success_message']    = getattr(file_import, 'success_message')
						kwargs_functions['failure_message']    = getattr(file_import, 'failure_message')
						new_command_set.split_to_commands(**kwargs_functions)
					# grabbing the top level steps
					elif thing_name.startswith('steps'):
						new_command_set = CommandSet()
						kwargs[thing_name]           = getattr(file_import, thing_name)
						kwargs['info_message']       = getattr(file_import, 'info_message')
						kwargs['success_message']    = getattr(file_import, 'success_message')
						kwargs['failure_message']    = getattr(file_import, 'failure_message')
						#command_pool[file_import.__name__] = CommandSet(**kwargs)
						new_command_set.split_to_commands(**kwargs)

					else:
						print(thing_name)
						kwargs[thing_name] = getattr(file_import, thing_name)
					#if thing_name not in basic_items:
					#	kwargs_single_command[thing_name] = getattr(file_import, thing_name)

			#kwargs done
			if len(kwargs) > 0:
				#TODO: gotta find the right name and set it
				#command_pool[file_import.__name__] = CommandSet(**kwargs)
			for function_name,function_object in kwargs_functions.items():
				new_command_set = CommandSet(**kwargs)
				setattr(new_command_set,function_name,function_object)
				command_pool[function_name] = new_command_set
			return command_pool

		except Exception as derp:
			self.error_exit('[-] CRITICAL ERROR: input file didnt validate, check your syntax maybe?', derp)

	###################################################################################
	## Dynamic imports
	###################################################################################
	def dynamic_import(self, module_to_import:str):
		'''
		Dynamically imports a module
			- used for the extensions

		Usage:
			thing = class.dynamic_import('name_of_file')
			returns a CommandSet()
		''' 
		command_files_name 	= 'pybashy.libraries.' + module_to_import
		imported_file		= import_module(command_files_name)#, package='pybashy')
		command_pool_dict = self.get_functions(imported_file)
		return command_pool_dict
		#kwargs = self.get_functions(imported_file)
		#new_command_set = CommandSet(kwargs)
		#return new_command_set

###############################################################################
###############################################################################
#class Stepper:
#getattr, setattr and self.__dict__
#	'''
#Steps through the command
#	'''
