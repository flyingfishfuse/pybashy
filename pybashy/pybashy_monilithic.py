
TESTING = True
import sys,os
import logging
import pkgutil
import inspect
import traceback
import subprocess
from pathlib import Path
from importlib import import_module

is_method = lambda func: inspect.getmembers(func, predicate=inspect.ismethod)
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

basic_items  = ['__name__', 'steps','success_message', 'failure_message', 'info_message']

class Command():
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

    def __repr__(self):
        greenprint("Command:")
        print(self.name)
        greenprint("Command String:")
        print(self.cmd_line)

class CommandSet():
    ''' metaclass'''
    #def __new__(cls):
    #    ''' waaat'''
    #    cls.name         = str
    #    cls.__name__     = cls.name
    #    cls.__qualname__ = cls.__name__
       
    def __init__(self):
        ''' waaat'''
        self.name         = str
        self.__name__     = self.name
        self.__qualname__ = self.__name__
    
    def __repr__(self):
        yellow_bold_print("HI! I AM A CommandSet()!")
    
    @classmethod
    def add_command_dict(cls, cmd_name, new_command_dict):
        try:
            new_command = Command(cmd_name, new_command_dict)
            setattr(cls , new_command.name, new_command)
        except Exception:
            error_printer('[-] Interpreter Message: CommandSet() Could not Init')  

class FunctionSet(CommandSet):
    '''This is just a CommandSet under a different name'''
    def __init__(self):
        '''This is a functionSet()'''
        # I shouldn't have to declare this twice, why did it not work?!?!
        self.name         = str
        self.__name__     = self.name
        self.__qualname__ = self.__name__
        
    def __repr__(self):
         yellow_bold_print("HI! I AM A FunctionSet() ")

class ModuleSet(CommandSet):
    ''' This is the class that gets multiple CommandSet() assignments
    assigned to it. It is a python representation of the input file JSON.
    Remember, python will change things in that file as it loads it'''
    def __init__(self,new_module_name):
        '''this is a ModuleSet() '''
        self.name         = new_module_name
        self.__name__     = self.name
        self.__qualname__ = self.__name__

    def __repr__(self):
         yellow_bold_print("HI! I AM A ModuleSet() ")

    def add_function(self, function_set : FunctionSet):
        function_name = function_set.name
        setattr(self, function_name, function_set)

class ExecutionPool():
    def __init__(self):
        '''todo : get shell/environ setup and CLEAN THIS SHIT UP MISTER'''
        self.set_actions = {}

    def get_actions_from_set(self, command_set):
        for attribute in command_set.items():
            if attribute.startswith("__") != True:
                self.set_actions.update({attribute : getattr(command_set,attribute)})

    def run_set(self, command_set : CommandSet):
        for command_name, command_object in command_set.items:
            print(command_name)
            command_line    = getattr(command_object,'cmd_line')
            success_message = getattr(command_object,'success_message')
            failure_message = getattr(command_object,'failure_message')
            info_message    = getattr(command_object,'info_message')
            yellow_bold_print(info_message)
            try:
                self.exec_command(command_line)
                print(success_message)
            except Exception:
                error_printer(failure_message)

    def run_function(self,command_set, function_to_run ):
        '''
        Feed it a CommandSet object and function name
        Remember, everything is strings in dicts until runtime
        ... Actually... thats pretty much all of python lol
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
                self.exec_command(command_line)
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
will create everything from the file and pop it all into an:
    - ExecutionPool()

SO...
    spiffy = ExecutionPool()
    lolwat = CommandRunner(exec_pool = spiffy)
    lolwat.get_stuff('commandtest')

Will return an ExecutionPool containing commandtest.py stuff
In a variable named spiffy

    '''
    def __init__(self, exec_pool : ExecutionPool):
        '''dooo eeeetttt'''

    def get_stuff(self, file_import):
        '''asdf'''
        try:
            imported_file = dir(file_import)
            module_set    = ModuleSet(imported_file.__name__)
            for thing_name in imported_file:
                if is_method(thing_name) and thing_name.startswith('__') != True:
                    # create a new Function(CommandSet)
                    if thing_name.startswith('function'):
                        # set function name
                        new_function       = FunctionSet()
                        new_function.name  = thing_name.strip('function_')
                        function_internals = dir(getattr(file_import, thing_name))
                        for param in function_internals:
                            if param == "steps" :
                                for command_name in param.keys():
                                    cmd_dict = param.get(command_name)
                                    new_function.add_command_dict(command_name,cmd_dict)
                        #add the function to the ModuleSet()
                        module_set.add_function(new_function)
            # now we assign top level steps and stuff to the ModuleSet()
            steps = getattr(file_import,"steps")
            for command_name in steps.keys():
                cmd_dict = param.get(command_name)
                # add the command to the function, set command name
                module_set.add_command_dict(command_name,cmd_dict)
            #add module to execution pool
            setattr(exec_pool, module_set.__name__, module_set)
        except SystemExit:
                error_printer('[-] CRITICAL ERROR: input file didnt validate, check your syntax maybe?')

    def dynamic_import(self, module_to_import:str):
        '''class.dynamic_import('name_of_file')''' 
        command_files_name     = 'pybashy.libraries.' + module_to_import
        imported_file          = import_module(command_files_name)#, package='pybashy')
        return imported_file

def object_inspector(object_to_inspect):
    inspect.getmembers(object_to_inspect, predicate=inspect.ismethod)

greenprint('==============================')
critical_message('-----[+] BEGINNING TEST! -----')
greenprint('==============================')
cmdstrjson = {'ls_etc' : { "command": "ls -la /etc","info_message":"[+] Info Text","success_message" : "[+] Command Sucessful", "failure_message" : "[-] ls -la Failed! Check the logfile!"},'ls_home' : { "command" : "ls -la ~/","info_message" : "[+] Info Text","success_message" : "[+] Command Sucessful","failure_message" : "[-] ls -la Failed! Check the logfile!"}}
exec_pool          = ExecutionPool()
module_set         = ModuleSet('test1')
function_prototype = CommandSet()
new_function       = FunctionSet()
runner = CommandRunner(exec_pool = exec_pool)
#runner.get_stuff("test.py")
for command_name in cmdstrjson.keys():
    cmd_dict = cmdstrjson.get(command_name)
    critical_message('[+] Adding command_dict to FunctionSet()')
    new_function.add_command_dict(command_name,cmd_dict)

    critical_message('[+] Adding command_dict to ModuleSet()')
    module_set.add_command_dict(command_name, cmdstrjson.get(command_name))

    critical_message('[+] Adding FunctionSet() to ModuleSet()')
    module_set.add_function(new_function.name)
        
    critical_message('[+] Adding ModuleSet() to ExecutionPool()')
    setattr(exec_pool, module_set.__name__, module_set)

trace_of_issue ='''
Traceback (most recent call last):
  File "./pybashy_monilithic.py", line 296, in <module>
    module_set.add_function(new_function.name)
  File "./pybashy_monilithic.py", line 150, in add_function
    function_name = function_set.name
AttributeError: type object 'str' has no attribute 'name'

'''