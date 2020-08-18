import os
import pkgutil
from importlib import import_module

from commandset import CommandSet
from useful_functions import greenprint,yellow_bold_print,redprint
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
		command_pool = {}
		for thing in dir(file_import):
		# filter out other stuff
			if thing.startswith('__') != True:
				commandset = thing
				if commandset.startswith('function'):
					#assign function to value
					kwargs_functions[commandset] = getattr(file_import, commandset)
				kwargs[commandset] = getattr(file_import, commandset)
		#kwargs done
		if len(kwargs) > 0:
			new_command_set = CommandSet()
			new_command_set.add_commands(kwargs)
			command_pool['test'] = new_command_set
		#print(kwargs )
		for function_name,function_object in kwargs_functions.items():
			new_command_set = CommandSet()
			setattr(new_command_set,function_name,function_object)
			command_pool[function_name] = new_command_set
			kwargs = command_pool
			new_command_set.add_commands(kwargs)
		for each in command_pool:
			print(each)
			for thing in dir(each):
				print(thing)
		# {'function_test_function1': <function function_test_function1>, 'function_test_function2': <function function_test_function2 >}
		#print(kwargs_loose_dicts)
		# now convert everything to wkargs for commandset
		#
		#return new_command_set
		
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
		self.get_functions(imported_file)
		#kwargs = self.get_functions(imported_file)
		#new_command_set = CommandSet(kwargs)
		#return new_command_set