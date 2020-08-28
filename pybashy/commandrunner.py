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
import typing
import pkgutil
import threading
import subprocess
from pathlib import Path
from importlib import import_module
from pybashy.useful_functions import greenprint,yellow_bold_print,redprint
from pybashy.useful_functions import info_message,warning_message,critical_message
from pybashy.useful_functions import error_message, error_exit

basic_items  = ['__name__', 'steps','success_message', 'failure_message', 'info_message']
script_cwd   = Path().absolute()
script_osdir = Path(__file__).parent.absolute()
###############################################################################
###############################################################################
class ExecutionPool():
	'''
	This is the command pool threading class, a container I guess?
	I dunno, I change things fast and loose
	'''
	def __init__(self):
		self.command_set_dict = {'test_init': Command({'test1' : ['ls -la ~/','info','pass','fail']})}
	
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
					if thing.startswith('__') != True:
						if thing.startswith('function') and thing.endswith(pollen):
							self.success_message = getattr(thing,'success_message')
							self.failure_message = getattr(thing,'failure_message')
							self.info_message	 = getattr(thing,'info_message')
							self.steps			 = getattr(thing,'steps')
							stepper = self.step(self.steps)
							if isinstance(stepper, Exception):
								error_exit(self.failure_message, Exception)
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
class Command:
	'''
	This class hold each individual step
	It is the direct translation/representation of :
		{'test1' : ['ls -la ~/','','','']}

	This is the bottom of the container chain
	 - ExecutionPool() -> CommandSet() -> Command(command : dict)
	'''
	def __init__(self,command: dict):
		self.cmd_line           = str
		self.info_message       = str
		self.success_message    = str
		self.failure_message    = str
		self.name               = str
		self.init_self(command)

	def init_self(self,command: dict):
		try:
			for command_name, command_action_set in command.items():
				self.name            = command_name
				self.cmd_line        = command_action_set[0]
				self.info_message    = command_action_set[1]
				self.success_message = command_action_set[2]
				self.failure_message = command_action_set[3]
		except Exception as derp:
			yellow_bold_print("[-] Instantiation of Command() Failed! One of these is not like the others!")
			return derp

	def __repr__(self):
		greenprint("Command:")
		print(self.name)
		greenprint("Command String:")
		print(self.cmd_line)

	def __name__(self):
		return self.name

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
	
		- then feed it to the BEEEEEE'S!
	'''
	#def __new__(cls, clsname, bases, clsdict):
	#	return super().__new__(cls, clsname, bases, clsdict)
	def __init__(self, kwargs):
		self.steps   	  = dict
		self.command_list = {}
		self.__name__     = str
		self.info_message       = str
		self.success_message    = str
		self.failure_message    = str
		for thing, value in kwargs.items():
			if thing == 'steps':
				for step_name, action_set in value:
					new_command = Command({step_name : action_set})
					self.command_list[step_name] = new_command
	
	def error_exit(self, message : str, derp):
		print(derp.with_traceback)
	
	def add_command(self, name, kwargs):
		self.command_list[name] = (Command(**kwargs))

	def list_commands(self):
		for command in self.command_list:
			print(command)

	def split_to_commands(self, kwargs):
		''' 
		feed it a thing, split it to Command()'s

		This method is for when you are adding steps : dict manually... 
		perhaps over the network? >.> hmmmm
		'''
		for thing, value in kwargs.items():
			if thing == 'steps':
				for step_name, action_set in value:
					self.command_list[step_name] = Command({step_name : action_set})


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

	def get_stuff(self, file_import):
		# we are differentiating between functions and other stuff
		# because we want to expand later
		kwargs 				= {}
		kwargs_function 	= {}
		execute_pool        = {}
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
						function_internals_list = dir(getattr(file_import, thing_name))
						for thing in basic_items:
							kwargs_function[thing] = getattr(function_internals_list,thing)
						new_command_set = CommandSet(**kwargs_function)
						execute_pool[thing_name.strip('function_')] = new_command_set
					# grabbing top level steps
					# along with the messages
					elif thing_name.startswith('steps'):
						for thing in basic_items:
							kwargs[thing] = getattr(file_import,thing)
						new_command_set = CommandSet(**kwargs)
						execute_pool[new_command_set.__name__] = new_command_set
					else:
						print(thing_name)
						# kwargs[thing_name] = getattr(file_import, thing_name)
			return execute_pool

		except Exception as derp:
			error_exit('[-] CRITICAL ERROR: input file didnt validate, check your syntax maybe?', message = derp)

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
		command_pool_dict   = self.get_stuff(imported_file)
		return command_pool_dict
		#kwargs = self.get_functions(imported_file)
		#new_command_set = CommandSet(kwargs)
		#return new_command_set

###############################################################################
###############################################################################
