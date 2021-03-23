# -*- coding: utf-8 -*-

"""
This is a most basic example of the command framework
    - you import this file with :
        
        new_command = CommandRunner()
        new_command.dynamic_import('commandtest')

    - All functions become thier own CommandSet()
        >>> isinstance(new_command, CommandSet())
        >>> True
        
        - from "steps" to "failure_message" is considered a CommandSet()
        - All "steps" are turned into Command() 's 
    
    - All CommandSet() are added to ExecutionPool()
    
    fields are as follows:
    - Name of Command
    - Command
    - Informational message to print
    - Success message
    - Failure message

Multiple commands can be placed in a dict, that are run sequentially:
{
           'ls_etc' : { "command"         : "ls -la /etc" ,
                        "info_message"    : "[+] Info Text",
                        "success_message" : "[+] Command Sucessful", 
                        "failure_message" : "[-] ls -la Failed! Check the logfile!"
                    },
            'ls_home' : { "command"         : "ls -la ~/"            ,
                          "info_message"    : "[+] Info Text"        ,
                          "success_message" : "[+] Command Sucessful", 
                          "failure_message" : "[-] ls -la Failed! Check the logfile!"
                        }
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

# OK WE ARE CHANGING IT ALL TO JSON FUCK IT ALL
steps = {
           'ls_etc' : { "command"         : "ls -la /etc" ,
                        "info_message"    : "[+] Info Text",
                        "success_message" : "[+] Command Sucessful", 
                        "failure_message" : "[-] ls -la Failed! Check the logfile!"
                    },
            'ls_home' : { "command"         : "ls -la ~/"            ,
                          "info_message"    : "[+] Info Text"        ,
                          "success_message" : "[+] Command Sucessful", 
                          "failure_message" : "[-] ls -la Failed! Check the logfile!"
                        }
          }

info_message    = "[+] Informational Text!"
success_message = "[+] Test Sucessful!"
failure_message = "[-] Test Failure!"


#multiple sets like this allowed
packages = 'lolcat'
apt_install = {
                'install_lolcat' : {
                    "command" : "sudo apt install lolcat" ,
                    "info_message"    : "[+] Info Text",
                    "success_message" : "[+] Command Sucessful", 
                    "failure_message" : "[-] ls -la Failed! Check the logfile!"
                    }
            }

#standalone command list as a name, not for any set or init
test1 = { 
           'ls_etc' : { "command"         : "ls -la /etc" ,
                        "info_message"    : "[+] Info Text",
                        "success_message" : "[+] Command Sucessful", 
                        "failure_message" : "[-] ls -la Failed! Check the logfile!"
                    },
            'ls_home' : { "command"         : "ls -la ~/"            ,
                          "info_message"    : "[+] Info Text"        ,
                          "success_message" : "[+] Command Sucessful", 
                          "failure_message" : "[-] ls -la Failed! Check the logfile!"
                        }
          }

# functions MUST START with "function"
# many of these allowed
# the whole function is considered a CommandSet()
def function_test_function1(params):
    steps = {
           'ls_etc' : { "command"         : "ls -la /etc" ,
                        "info_message"    : "[+] Info Text",
                        "success_message" : "[+] Command Sucessful", 
                        "failure_message" : "[-] ls -la Failed! Check the logfile!"
                    },
            'ls_home' : { "command"         : "ls -la ~/"            ,
                          "info_message"    : "[+] Info Text"        ,
                          "success_message" : "[+] Command Sucessful", 
                          "failure_message" : "[-] ls -la Failed! Check the logfile!"
                        }
          }
    # This displays as the command is about to run
    info_message    = "[+] Informational Text!"
    # herp
    success_message = "[+] Test Sucessful!"
    # a derp
    failure_message = "[-] Test Failure!"

def function_test_function2(params):
    steps = {
           'ls_etc' : { "command"         : "ls -la /etc" ,
                        "info_message"    : "[+] Info Text",
                        "success_message" : "[+] Command Sucessful", 
                        "failure_message" : "[-] ls -la Failed! Check the logfile!"
                    },
            'ls_home' : { "command"         : "ls -la ~/"            ,
                          "info_message"    : "[+] Info Text"        ,
                          "success_message" : "[+] Command Sucessful", 
                          "failure_message" : "[-] ls -la Failed! Check the logfile!"
                        }
          }
    info_message    = "[+] Informational Text!"
    success_message = "[+] Test Sucessful!"
    failure_message = "[-] Test Failure!"

class TestCommand1():
    '''
    everything gets preprocessed remember.
    When it's imported dynamically, this class 
    MUST be complete.
    Functions do not need be prepended with "function"
    '''
    def __init__(self):
        self.steps = {
           'ls_etc' : { "command"         : "ls -la /etc" ,
                        "info_message"    : "[+] Info Text",
                        "success_message" : "[+] Command Sucessful", 
                        "failure_message" : "[-] ls -la Failed! Check the logfile!"
                    },
            'ls_home' : { "command"         : "ls -la ~/"            ,
                          "info_message"    : "[+] Info Text"        ,
                          "success_message" : "[+] Command Sucessful", 
                          "failure_message" : "[-] ls -la Failed! Check the logfile!"
                        }
          }

        self.info_message    = "[+] Informational Text!"
        self.success_message = "[+] Test Sucessful!"
        self.failure_message = "[-] Test Failure!"
    def __repr__(self):
        print(self.steps)
