import os
import pkgutil
from importlib import import_module

from pybashy.commandset import CommandSet
from pybashy.useful_functions import greenprint,yellow_bold_print,redprint
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
		command_files_dir = os.path.dirname(__file__) + "/commandset"		
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
		command_pool        = {}
		kwargs_single_command = {}
		for thing_name in dir(file_import):
		# filter out other stuff
			if thing_name.startswith('__') != True:
				if thing_name.startswith('function'):
					#assign function to value
					kwargs_functions[thing_name] = getattr(file_import, thing_name)
				#everything_name else not internal to the import class
				else:
					print(thing_name)
					#assign the thing, with the name, to kwargs
					kwargs[thing_name] = getattr(file_import, thing_name)
				#if thing_name not in self.basic_items:
				#	kwargs_single_command[thing_name] = getattr(file_import, thing_name)
		#kwargs done
		if len(kwargs) > 0:
			new_command_set = CommandSet(kwargs)
			command_pool['top_level_steps'] = new_command_set
		
		command_pool[file_import.__name__] = CommandSet(kwargs_single_command)

		for function_name,function_object in kwargs_functions.items():
			new_command_set = CommandSet(kwargs)
			setattr(new_command_set,function_name,function_object)
			
			command_pool[function_name] = new_command_set

		return command_pool
		
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