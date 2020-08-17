import pkgutil
from importlib import import_module

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
		command_files_dir = os.path.dirname(__file__) + "/command_set"		
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
			thing = class.dynamic_import('name_of_file')
			returns a CommandSet()
		''' 
		kwargs 				= {}
		kwargs_functions 	= {}
		command_files_name 	= 'command_set.' + module_to_import
		imported_file		= import_module(command_files_name )#, package='pybashy')
		# dir just gets names:str
		# to get values of those things, you need getattr(obj,name)
		for thing in dir(imported_file):
			# filter out other stuff
			if thing.startswith('__') != True:
				commandset = thing
				# if the import has a function
				if commandset.startswith('function'):
					kwargs_functions[commandset] = getattr(imported_file, commandset)
					yellow_bold_print(commandset)
				# if the import contains a top level script
				elif commandset in basic_items:
					kwargs[commandset] = getattr(imported_file, commandset)
		new_command_set = CommandSet(kwargs)
		return new_command_set