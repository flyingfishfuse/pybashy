import os
import sys
import subprocess
from pathlib import Path
from importlib import import_module
from pybashy.CommandSet import CommandSet,Function,ModuleSet
from pybashy.ExecutionPool import ExecutionPool
from pybashy.internal_imports import error_printer
basic_items  = ['__name__', 'steps','success_message', 'failure_message', 'info_message']
script_cwd   = Path().absolute()
script_osdir = Path(__file__).parent.absolute()
####################################################
class CommandRunner:
    '''
NARF!
Goes running after commands
    '''
    def __init__(self):#,kwargs):
        #for (k, v) in kwargs.items():
        #    setattr(self, k, v)
        pass

    def get_stuff(self, file_import):
        '''
    This is used to import whole files as modules
    into a CommandSet() Object

    Functions go in thier own CommandSet() , to be added 
    as a named attribute
        '''
        top_level_steps   = {}
        function_command  = {}
        imported_file     = dir(file_import)
        module_cmd_set    = ModuleSet()
        # name set in the module 
        setattr(module_cmd_set.__name__, )
        try:
            for thing_name in imported_file:
                if thing_name.startswith('__') != True:
                    # create a new Function(CommandSet)
                    #assign it to module set
                    if thing_name.startswith('function'):
                        new_function       = Function()
                        new_function.name  = thing_name.strip('function_')
                        #grab function internals
                        function_internals = dir(getattr(file_import, thing_name))
                        for param in function_internals:
                            # if it is the dict of commands *cough*droids*cough* we are looking for
                            if param == "steps" :
                                #iterate over key,value pairs
                                for command in param.keys:
                                    new_attr_name  = command
                                    new_attr_value = param.get(command)
                                    new_function.__dict__.update({new_attr_name : new_attr_value})
                        for thing in basic_items:
                            #assign command dict to Command
                            function_command.update(getattr(function_internals,thing))
                        #add that command to the function

                        # add that function/command to the new CommandSet
                        module_cmd_set.add_command_dict(str.strip("function_",thing_name.__name__),function_command)
                        # add that CommandSet() to the Main CommandSet()
                        # representing the file/module itself

# you stopped working here dummy
                    exec_pool_addendum = {str.strip("function_",thing_name.__name__) : new_command_set}
                    # grabbing top level steps
                    try:
                        steps = getattr(file_import,"steps")
                        for key, value in steps:
                            top_level_steps.update({file_import.__name__ : { key : value}})
                        for thing in basic_items:
                            pass
                        #module_cmd_set = CommandSet()
                        #module_cmd_set.add_command_dict(**kwargs)
                    except Exception:
                        error_printer("[-] Failed to import Top Level Steps")
                    else:
                        print(thing_name)
                        # kwargs[thing_name] = getattr(file_import, thing_name)
        except SystemExit:
            error_printer('[-] CRITICAL ERROR: input file didnt validate, check your syntax maybe?')

    ###################################################################################
    ## Dynamic imports
    ###################################################################################
    def dynamic_import(self, module_to_import:str):
        '''
        Dynamically imports a module
            - used for the extensions

        Usage:
            class.dynamic_import('name_of_file')
        ''' 
        command_files_name     = 'pybashy.libraries.' + module_to_import
        imported_file          = import_module(command_files_name)#, package='pybashy')
        self.get_stuff(imported_file)


###############################################################################
###############################################################################
