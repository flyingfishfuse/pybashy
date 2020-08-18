import os
import pkgutil
from importlib import import_module

from commandset import CommandSet
from useful_functions import *
class CommandRunner:
	'''
NARF!
Goes running after commands
	'''
	def __init__(self):#,kwargs):
		#for (k, v) in kwargs.items():
		#	setattr(self, k, v)
		self.basic_items = ['steps','success_message', 'failure_message', 'info_message']


	def list_modules(self):
		'''
	Lists modules in command_set directory
		'''
		list_of_modules = []
		command_files_dir = os.path.dirname(__file__) + "/command_set"		
		list_of_subfiles  = pkgutil.iter_modules([command_files_dir])
		for x in list_of_subfiles:
			print(x.name)
			list_of_modules.append(x.name)
		return list_of_modules

#apt_install = { 'apt_install' 	: ["sudo -S apt install {}".format(packages), 
#					'info_message'		: "[+] Informational Text!",
#					'success_message'	: "[+] 	Sucessful!",
#					'failure_message'	: "[-] 	Failure!"]
#				}
	def get_functions(self, file_import):
		kwargs 				= {}
		kwargs_functions 	= {}
		kwargs_loose_dicts	= {}
		for thing in dir(file_import):
		# filter out other stuff
			if thing.startswith('__') != True:
				commandset = thing
				# if the import has a function
				if commandset.startswith('function'):
					kwargs_functions[commandset] = getattr(file_import, commandset)
					print(commandset)
				# if the import contains a loose dict
				elif isinstance(commandset, dict):
					command_array = commandset.items()
					print(commandset.items())
					info_message = command_array[1]
					success_message = command_array[2]
					failure_message = command_array[3]
					
					kwargs_loose_dicts[commandset] = getattr(file_import, commandset)
				#if the import IS a script
				# it has things at top already
				elif thing in self.basic_items:
					kwargs[commandset] = getattr(file_import,commandset)
		print(kwargs )
		print(kwargs_functions)
		print(kwargs_loose_dicts)
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
		command_files_name 	= 'command_set.' + module_to_import
		imported_file		= import_module(command_files_name)#, package='pybashy')
		#kwargs = self.get_functions(imported_file)
		#new_command_set = CommandSet(kwargs)
		#return new_command_set