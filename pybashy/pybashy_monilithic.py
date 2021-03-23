TESTING = True
import sys,os
import logging
import pkgutil
import traceback
import subprocess
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
        error_message( message + ''.join(trace.format_exception_only()))
        try:
            traceback.format_list(traceback.extract_tb(trace)[-1:])[-1]
        except Exception:
            error_message(trace.exc_traceback.tb_frame.f_code)
        debug_message('LINE NUMBER >>>' + str(exc_tb.tb_lineno))
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

class CustomException(Exception):
    '''Base Class for Internal Exception Labeling'''

class CommandFormatException(CustomException):
    '''Failure in the text of a Command(command_input)
    An internal Error unless you are feeding JSON directly
    to:
        - Command.init_self(json_str : json)'''
    def __init__(self, derp:str, errors):
        exc_type, exc_value, exc_tb = sys.exc_info()
        trace = traceback.TracebackException(exc_type, exc_value, exc_tb) 
        if LOGLEVEL == 'DEV_IS_DUMB':
            error_message( derp + ''.join(trace.format_exception_only()))
            critical_message(errors)
            try:
                traceback.format_list(traceback.extract_tb(trace)[-1:])[-1]
            except Exception:
                error_message(trace.exc_traceback.tb_frame.f_code)
            debug_message('LINE NUMBER >>>' + str(exc_tb.tb_lineno))
        else:
            error_message(derp + ''.join(trace.format_exception_only()))

#cmdstrjson = {'ls_etc' : {"command" : "ls -la /etc" , "info_message": "[+] Info Text", "success_message" : "[+] Command Sucessful", "failure_message" : "[-] ls -la Failed! Check the logfile!"}}
cmdstrjson = {'ls_etc' : { "command": "ls -la /etc","info_message":"[+] Info Text","success_message" : "[+] Command Sucessful", "failure_message" : "[-] ls -la Failed! Check the logfile!"},'ls_home' : { "command" : "ls -la ~/","info_message" : "[+] Info Text","success_message" : "[+] Command Sucessful","failure_message" : "[-] ls -la Failed! Check the logfile!"}}
basic_items  = ['__name__', 'steps','success_message', 'failure_message', 'info_message']

class Command():
    def __new__(cls):
        cls.__name__ = str
        cls.cmd_line           = str
        cls.info_message       = str
        cls.success_message    = str
        cls.failure_message    = str
        cls.name               = str
        return super().__new__(cls)
    def __init__(self):
        '''init stuff'''
    def init_self(self,command_struct: dict):
        '''
        ONLY ONE COMMAND, WILL THROW ERROR IF NOT TO SPEC
        '''
        try:
            # name self after the command
            for key in command_struct.keys():
                self.name        = key
            # use that to grab the internals
            internals = command_struct.get(self.name)
            self.cmd_line        = internals.get("command")
            self.info_message    = internals.get("info_message")
            self.success_message = internals.get("success_message")
            self.failure_message = internals.get("failure_message")
        except CommandFormatException("[-] Command Failed to MATCH SPECIFICATION", command_struct):
            pass
    
    
    def __repr__(self):
        greenprint("Command:")
        print(self.name)
        greenprint("Command String:")
        print(self.cmd_line)

    def __name__(self):
        return self.name

class CommandSet():
    ''' metaclass'''
    def __new__(cls,name):
        cls.name = name
    def __init__(self,name):
        ''' waaat'''
        #self.__dict__.update({'name': name})
    def __name__(self):
        return self.name
    def add_command_dict(self, new_command_dict:dict):
        try:
            new_command = Command()
            for command_name, command_container in new_command_dict.items():
                new_command.init_self({command_name : command_container})
                setattr(self , new_command.name, new_command)
        except Exception:
            error_printer('[-] Interpreter Message: CommandSet() Could not Init')  
            sys.exit()

    def add_function(self, command_set : CommandSet):
        '''
        Assigns a CommandSet() Object to self for the purposes
        of having "functions" be thier own sets of commands
        '''
        self.__dict__.update({command_set.name : command_set})


class ModuleSet(CommandSet):
    def __init__(self,new_command_set_name):
        self.__dict__.update({'name':new_command_set_name})
    def __name__(self):
        return self.name
    def add_function(self, command_set : CommandSet):
        cmd_name = command_set.__name__
        self.__dict__.update( { cmd_name : command_set } )

class FunctionSet(CommandSet):
    def __init__(self):
        '''BLARP!'''

class ExecutionPool():
    def __init__(self):
        '''asdf'''
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
        #read, write = os.pipe()
#        step = subprocess.Popen(something_to_set_env, 
#                        shell=shell_env, 
#                        stdin=read, 
#                        stdout=sys.stdout, 
#                        stderr=subprocess.PIPE)
#        Note that this is limited to sending a maximum of 64kB at a time,
#         pretty much an interactive session
#        byteswritten = os.write(write, str(command))
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
            yellow_bold_print("[-] Interpreter Message: exec_command() failed!")
            return derp

new_command_set = CommandSet('test1')
new_function = FunctionSet('testfunc')

for command in cmdstrjson.keys:
    new_command_set.add_command_dict(command.get())
    new_attr_name  = command

new_attr_value = command.get(new_attr_name)
new_function.__dict__.update({new_attr_name : new_attr_value})

execution_pool = ExecutionPool()
command_runner = CommandRunner()
command_pool   = command_runner.dynamic_import('commandtest')
# printing the contents