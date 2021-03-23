import os
import sys
import subprocess
from pathlib import Path
from importlib import import_module
from pybashy.CommandSet import CommandSet
from pybashy.ExecutionPool import ExecutionPool
from pybashy.useful_functions import error_printer
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
        top_level_steps   = {}
        function_command  = {}
        imported_file     = dir(file_import)
        new_command_set   = CommandSet()
        setattr(new_command_set.__name__, )
        try:
            for thing_name in imported_file:
                if thing_name.startswith('__') != True:
                    if thing_name.startswith('function'):
                        function_internals_list = dir(getattr(file_import, thing_name))
                        for thing in basic_items:
                            #assign command dict to Command
                            function_command.update(getattr(function_internals_list,thing))
                        # add that function/command to the new CommandSet
                        new_command_set = CommandSet()
                        new_command_set.add_command_dict(str.strip("function_",thing_name.__name__),function_command)
                        # add that CommandSet() to the ExecutionPool Named as itself
                       

# you stopped working here dummy
                    exec_pool_addendum = {str.strip("function_",thing_name.__name__) : new_command_set}
                    # grabbing top level steps
                    try:
                        steps = getattr(file_import,"steps")
                        for key, value in steps:
                            top_level_steps.update({file_import.__name__ : { key : value}})
                        for thing in basic_items:
                            pass
                        new_command_set = CommandSet()
                        new_command_set.add_command_dict(**kwargs)
                    except Exception:
                        error_printer("[-] Failed to import Top Level Steps")
                    else:
                        print(thing_name)
                        # kwargs[thing_name] = getattr(file_import, thing_name)
            return execute_pool

        except SystemExit:
            error_printer('[-] CRITICAL ERROR: input file didnt validate, check your syntax maybe?', message = derp)

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
        command_files_name     = 'pybashy.libraries.' + module_to_import
        imported_file        = import_module(command_files_name)#, package='pybashy')
        command_pool_dict   = self.get_stuff(imported_file)
        return command_pool_dict
        #kwargs = self.get_functions(imported_file)
        #new_command_set = CommandSet(kwargs)
        #return new_command_set

###############################################################################
###############################################################################
