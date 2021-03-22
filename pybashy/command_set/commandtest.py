# -*- coding: utf-8 -*-

"""
This is a most basic example of the command framework

OH MYYY, new work, adding classes and inventing "inherritance"

    - you import this file with :
        
        new_command = CommandRunner()
        new_command.dynamic_import('commandtest')

    - All functions become thier own CommandSet()
        >>> isinstance(new_command, CommandSet())
        >>> True
        
        - from "steps" to "failure_message" is considered a CommandSet()
        - All "steps" are turned into Command() 's 
    
    - All CommandSet() are added to ExecutionPool()

    - To Retrieve a list of loaded CommandSet() and thier operations, use:
        - ExecutionPool.list_operations(new_command) 
        - ExecutionPool.list_commands()

    - to run the execution pool, you use the worker_bee() function:

        finished_command = new_command.worker_bee(ExecutionPool(command))


Every command is a dict with an array of four string fields as the value:
    
    {'test1' : ['ls -la ~/','','','']}
    
    Array fields are as follows:
    - Name of Command
    - Command
    - Informational message to print
    - Success message
    - Failure message

Multiple commands can be placed in a dict, that are run sequentially:
    {
        'test1' : ['ls -la ~/','','',''],
        'test2' : ['ls -la ~/','','','']
    }



"""
__author__ = 'Adam Galindo'
__email__ = 'null@null.com'
__version__ = '1'
__license__ = 'GPLv3'


# EVERY MODULE MUST HAVE A __name__!!!
__name__  = "CommandTestModule"

# from "steps" to "failure_message" 
# is considered a CommandSet()
# only one set like this allowed, I guess this would be used for setup operations 
# and teardown staging
steps = { 'ls_user' : ["ls -la ~/", "[+] Info Text",
                                    "[+] Command Sucessful", 
                                    "[-] Command Failed! Check the logfile!"],
          'ls_root' : ["ls -la /",    "[+] Info Text",
                                      "[+] Command Sucessful!", 
                                    "[-] Command Failed! Check the logfile!"],
          'ls_etc'  : ["ls -la /etc","[+] Info Text",
                                      "[+] Command Sucessful", 
                                    "[-] ls -la Failed! Check the logfile!"]
            }
info_message    = "[+] Informational Text!"
success_message = "[+] Test Sucessful!"
failure_message = "[-] Test Failure!"


#multiple sets like this allowed
packages = 'lolcat'
apt_install = { 
                'test1': ["sudo apt install {}".format(packages),
                                'Informational Text!',
                                "[+]Sucessful!",
                                "[-]Failure!"]
                }

test1 = {'test1' : ['ls -la ~/','info','pass','fail']}
# functions MUST START with "function"
# many of these allowed
# the whole function is considered a CommandSet()
def function_test_function1(params):
    steps = { 
                'ls_user' : ["ls -la ~/",     "[+] Info Text",
                                            "[+] Command Sucessful", 
                                            "[-] Command Failed! Check the logfile!"],
               'ls_root' : ["ls -la /",        "[+] Info Text",
                                               "[+] Command Sucessful!", 
                                            "[-] Command Failed! Check the logfile!"],
               'ls_etc'  : ["ls -la /etc",    "[+] Info Text",
                                               "[+] Command Sucessful", 
                                            "[-] ls -la Failed! Check the logfile!"]
            }
    # This displays as the command is about to run
    info_message    = "[+] Informational Text!"
    # herp
    success_message = "[+] Test Sucessful!"
    # a derp
    failure_message = "[-] Test Failure!"

def function_test_function2(params):
    steps = { 
                'ls_user' : ["ls -la ~/", "[+] Info Text",
                                        "[+] Command Sucessful", 
                                        "[-] Command Failed! Check the logfile!"],
                'ls_root' : ["ls -la /", "[+] Info Text",
                                           "[+] Command Sucessful!",
                                        "[-] Command Failed! Check the logfile!"],
                'ls_etc'  : ["ls -la /etc","[+] Info Text",
                                           "[+] Command Sucessful",
                                        "[-] ls -la Failed! Check the logfile!"]
            }
    info_message    = "[+] Informational Text!"
    success_message = "[+] Test Sucessful!"
    failure_message = "[-] Test Failure!"

# AND NOW!!!!
# WE CAN DO....

# THIS!
class TestCommand1():
    '''
    everything gets preprocessed remember.
    When it's imported dynamically, this class 
    MUST be complete.
    Functions do not need be prepended with "function"
    '''
    def __init__(self):
        self.steps = { 
            'ls_user' : ["ls -la ~/", "[+] Info Text",
                                    "[+] Command Sucessful", 
                                    "[-] Command Failed! Check the logfile!"],
            'ls_root' : ["ls -la /", "[+] Info Text",
                                    "[+] Command Sucessful!",
                                    "[-] Command Failed! Check the logfile!"],
            'ls_etc'  : ["ls -la /etc","[+] Info Text",
                                    "[+] Command Sucessful",
                                    "[-] ls -la Failed! Check the logfile!"]
            }
        self.info_message    = "[+] Informational Text!"
        self.success_message = "[+] Test Sucessful!"
        self.failure_message = "[-] Test Failure!"
    def __repr__(self):
        print(self.steps)
