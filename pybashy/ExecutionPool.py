import os
import sys
import subprocess
from pathlib import Path
from pybashy.useful_functions import yellow_bold_print,info_message
from pybashy.useful_functions import critical_message,error_printer
import pybashy.CommandSet
from pybashy.CommandSet import CommandSet
script_cwd   = Path().absolute()
script_osdir = Path(__file__).parent.absolute()
###############################################################################
###############################################################################
class ExecutionPool():
    '''

    '''
    def __init__(self):
        # always testing for code change validation
        # this is the expected workflow
        try:
            test_command = {'test1' : ['ls -la ~/','info','pass','fail']}
            test1 = CommandSet()
            # we only add ONE DICT!!!
            # then we append that to the execution pool container
            # uhhhh ... I think it changes it's own name? lolz
            # FIND THE CODE TO GET THE NAME!
            self.command_set_dict = {test1.add_command_dict(test_command.__name__, test_command): test1}
        except Exception:
            error_printer("[-] Failure in ExecutionPool.__init__ during test")

    
    def step(self, command : dict):
        '''
this is run by self.run_runction and should not be 
accessed directly unless you are supplying a basic 
command dict of the form :
    test_command = {'command_name' : ['ls -la ~/','info','pass','fail']}
        '''
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

###############################################################################
###############################################################################

