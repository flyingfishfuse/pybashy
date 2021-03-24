
TESTING = True
import sys,os
import logging
import pkgutil
import inspect
import traceback
import subprocess
from pathlib import Path
from importlib import import_module

script_cwd   = Path().absolute()
script_osdir = Path(__file__).parent.absolute()
try:
    import colorama
    from colorama import init
    init()
    from colorama import Fore, Back, Style
    if TESTING == True:
        COLORMEQUALIFIED = True
except ImportError as derp:
    print("[-] NO COLOR PRINTING FUNCTIONS AVAILABLE, Install the Colorama Package from pip")
    COLORMEQUALIFIED = False

blueprint= lambda text: print(Fore.BLUE + ' ' +  text + ' ' + Style.RESET_ALL) if (COLORMEQUALIFIED == True) else print(text)
greenprint= lambda text: print(Fore.GREEN + ' ' +  text + ' ' + Style.RESET_ALL) if (COLORMEQUALIFIED == True) else print(text)
redprint= lambda text: print(Fore.RED + ' ' +  text + ' ' + Style.RESET_ALL) if (COLORMEQUALIFIED == True) else print(text)

makered= lambda text: Fore.RED + ' ' +  text + ' ' + Style.RESET_ALL if (COLORMEQUALIFIED == True) else None
makegreen= lambda text: Fore.GREEN + ' ' +  text + ' ' + Style.RESET_ALL if (COLORMEQUALIFIED == True) else None
makeblue= lambda text: Fore.BLUE + ' ' +  text + ' ' + Style.RESET_ALL if (COLORMEQUALIFIED == True) else None
makeyellow= lambda text: Fore.YELLOW + ' ' +  text + ' ' + Style.RESET_ALL if (COLORMEQUALIFIED == True) else None
yellow_bold_print= lambda text: print(Fore.YELLOW + Style.BRIGHT + ' {} '.format(text) + Style.RESET_ALL) if (COLORMEQUALIFIED == True) else print(text)

LOGLEVEL = 'DEV_IS_DUMB'
LOGLEVELS = [1,2,3,'DEV_IS_DUMB']

log_file  = 'garden_grid_message_log'
logging.basicConfig(filename=log_file, format='%(asctime)s %(message)s', filemode='w')
logger    = logging.getLogger()

debug_message = lambda message: logger.debug(blueprint(message)) 
info_message  = lambda message: logger.info(greenprint(message))   
warning_message  = lambda message: logger.warning(yellow_bold_print(message)) 
error_message    = lambda message: logger.error(redprint(message)) 
critical_message = lambda message: logger.critical(yellow_bold_print(message))

def error_printer(message):
    exc_type, exc_value, exc_tb = sys.exc_info()
    trace = traceback.TracebackException(exc_type, exc_value, exc_tb) 
    if LOGLEVEL == 'DEV_IS_DUMB':
        debug_message('LINE NUMBER >>>' + str(exc_tb.tb_lineno))
        greenprint('[+]The Error That Occured Was :')
        error_message( message + ''.join(trace.format_exception_only()))
        try:
            critical_message("Some info:")
            makegreen(traceback.format_tb(trace.exc_traceback))
            #makegreen(traceback.format_list(traceback.extract_tb(trace)[-1:])[-1])
        except Exception:
            critical_message("Some Info- exception:")
    else:
        error_message(message + ''.join(trace.format_exception_only()))

def list_modules():
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

#cmdstrjson = {'ls_etc' : {"command" : "ls -la /etc" , "info_message": "[+] Info Text", "success_message" : "[+] Command Sucessful", "failure_message" : "[-] ls -la Failed! Check the logfile!"}}
cmdstrjson = {'ls_etc' : { "command": "ls -la /etc","info_message":"[+] Info Text","success_message" : "[+] Command Sucessful", "failure_message" : "[-] ls -la Failed! Check the logfile!"},'ls_home' : { "command" : "ls -la ~/","info_message" : "[+] Info Text","success_message" : "[+] Command Sucessful","failure_message" : "[-] ls -la Failed! Check the logfile!"}}
basic_items  = ['__name__', 'steps','success_message', 'failure_message', 'info_message']

class Command():
    #def __new__(cls):
        #cls.__name__           = ''
        #cls.cmd_line           = str
        #cls.info_message       = str
        #cls.success_message    = str
        #cls.failure_message    = str
        #return super().__new__(cls)

    def __init__(self, cmd_name , command_struct):
        '''init stuff
        ONLY ONE COMMAND, WILL THROW ERROR IF NOT TO SPEC
        '''
        self.name                = cmd_name
        try:
            self.cmd_line        = command_struct.get("command")
            self.info_message    = command_struct.get("info_message")
            self.success_message = command_struct.get("success_message")
            self.failure_message = command_struct.get("failure_message")
        except Exception:
            error_printer("[-] JSON Input Failed to MATCH SPECIFICATION!\n\n    ")

    #def init_self(self,command_struct: dict):
            #for key in command_struct.keys():
            #    self.name        = key
        #return self
    
    def __repr__(self):
        greenprint("Command:")
        print(self.name)
        greenprint("Command String:")
        print(self.cmd_line)

    def __name__(self):
        return self.name

class CommandSet():
    ''' metaclass'''
    #def __new__(cls):
    #    cls.name = ''
    #    return cls
    
    def __init__(self):
        ''' waaat'''
        self.name = str

    def __name__(self):
        return self.name
    
    def add_command_dict(self, cmd_name, new_command_dict):
        try:
            new_command = Command(cmd_name, new_command_dict)
            #for command_name, command_container in new_command_dict.items():
            #    new_command.init_self({command_name : command_container})
            #    setattr(self , new_command.name, new_command)
            #new_command.init_self(new_command_dict)
            setattr(self , new_command.name, new_command)
        except Exception:
            error_printer('[-] Interpreter Message: CommandSet() Could not Init')  
            #sys.exit()
#        return self

class ModuleSet(CommandSet):
    ''' This is the class that gets multiple CommandSet() assignments'''
    def __init__(self,new_command_set_name):
        '''narf '''
        self.name = new_command_set_name

    def __name__(self):
        return self.name
    
    def add_function(self, command_set : CommandSet):
        cmd_name = command_set.name
        self.__dict__.update( { cmd_name : command_set } )
        #return self

class FunctionSet(CommandSet):
    '''This is just a CommandSet under a different name'''
    def __init__(self):
        '''BLARP!'''
    def __name__(self):
        return self.name


class ExecutionPool():
    def __init__(self):
        '''todo : get shell/environ setup and CLEAN THIS SHIT UP MISTER'''
    def step(self, command : dict):
        '''asdf'''
        try:
            for name, action_set in command.items():
                cmd     = action_set[0]
                info    = action_set[1]
                success = action_set[2]
                fail    = action_set[3]
                yellow_bold_print(info)
                self.current_command = cmd
                cmd_exec = self.exec_command(self.exec_command(name))
                if cmd_exec.returncode == 0 :
                    info_message(success)
                else:
                    raise OSError.with_traceback()
        except Exception:
            error_printer(fail)

    def run_set(self, command_set : CommandSet):
        for command_name, command_object in command_set.command_list.items():
            print(command_name)
            command_line    = getattr(command_object,'cmd_line')
            success_message = getattr(command_object,'success_message')
            failure_message = getattr(command_object,'failure_message')
            info_message    = getattr(command_object,'info_message')
            yellow_bold_print(info_message)
            try:
                self.step(command_line)
                print(success_message)
            except Exception:
                error_printer(failure_message)

    def run_function(self,command_set, function_to_run ):
        '''
        '''
        try:
            #requesting a specific Command()
            command_object  = command_set.command_list.get(function_to_run)
            command_line    = getattr(command_object,'cmd_line')
            success_message = getattr(command_object,'success_message')
            failure_message = getattr(command_object,'failure_message')
            info_message    = getattr(command_object,'info_message')
            yellow_bold_print(info_message)
            try:
                self.step(command_line)
                print(success_message)
            except Exception:
                error_printer(failure_message)
            # running the whole CommandSet()
        except Exception:
            error_printer(failure_message)

    def exec_command(self, command, blocking = True, shell_env = True):
        '''TODO: add formatting'''
        try:
            if blocking == True:
                step = subprocess.Popen(command,shell=shell_env,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
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
            yellow_bold_print("[-] Interpreter Message: exec_command() failed!")
            return derp

class CommandRunner:
    '''
NARF!
Goes running after commands
use like :
    - CommandRunner.dynamic_import('name_of_file')
And it will create everything from the file and pop it all into an:
    - ExecutionPool()

SO...
    - asdf = CommandRunner.dynamic_import('commandtest')
        Will return an ExecutionPool containing commandtest.py stuff
    '''
    def __init__(self):#,kwargs):
        '''dooo eeeetttt'''
    def get_stuff(self, file_import):
        '''asdf'''
        try:
            imported_file = dir(file_import)
            module_set    = ModuleSet(imported_file.__name__)
            # name set in the module 
            #setattr(module_cmd_set.__name__, )
            for thing_name in imported_file:
                is_method = lambda func: inspect.getmembers(func, predicate=inspect.ismethod)
                if is_method(thing_name) and thing_name.startswith('__') != True:
                    # create a new Function(CommandSet)
                    #assign it to module set
                    if thing_name.startswith('function'):
                        # set function name
                        new_function       = FunctionSet()
                        new_function.name  = thing_name.strip('function_')
                        #grab function internals from imported module/file
                        function_internals = dir(getattr(file_import, thing_name))
                        for param in function_internals:
                            # if it is the dict of commands *cough*droids*cough* we are looking for
                            if param == "steps" :
                                #iterate over {command name , JSON payload} pairs
                                for command_name in param.keys():
                                    cmd_dict = param.get(command_name)
                                    # add the command to the function, set command name
                                    new_function.add_command_dict(command_name,cmd_dict)
                                    #new_command_set.__dict__.update({new_attr_name : new_attr_value})
                        #add the function to the ModuleSet()
                        module_set.add_function(new_function)
                    # now we assign top level steps and stuff to the ModuleSet()
                #    for thing in basic_items:
                #        if thing_name == "steps":
            steps = getattr(file_import,"steps")
            for command_name in steps.keys():
                cmd_dict = param.get(command_name)
                # add the command to the function, set command name
                module_set.add_command_dict(command_name,cmd_dict)
                # you stopped working here dummy
                    #exec_pool_addendum = {str.strip("function_",thing_name.__name__) : new_command_set}
        except SystemExit:
                error_printer('[-] CRITICAL ERROR: input file didnt validate, check your syntax maybe?')

    ###################################################################################
    ## Dynamic imports
    ###################################################################################
    def dynamic_import(self, module_to_import:str):
        '''class.dynamic_import('name_of_file')''' 
        command_files_name     = 'pybashy.libraries.' + module_to_import
        imported_file          = import_module(command_files_name)#, package='pybashy')
        self.get_stuff(imported_file)

greenprint('==============================')
critical_message('-----[+] BEGINNING TEST! -----')
greenprint('==============================')
try:
    exec_pool          = ExecutionPool()
    #creating a function
    function_prototype = CommandSet()
    # we going to assign it to a functionset
    new_function       = FunctionSet()
    
    greenprint("[+] Command name:")

    for command_name in cmdstrjson.keys():
        print(command_name)
        function_prototype.name = command_name
        greenprint("function prototype name")
        print(function_prototype.name)
        cmd_dict = cmdstrjson.get(command_name)
        greenprint("command dict")
        print(cmd_dict)
        # create the function
        function_prototype.add_command_dict(command_name, cmd_dict)
        # put the function in a
        new_function.add_command_dict(command_name,cmd_dict)
        #inspect.getmembers(function_prototype, predicate=inspect.ismethod)
except Exception:
    error_printer("WARGLEBARGLE!")