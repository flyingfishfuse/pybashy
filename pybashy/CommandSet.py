#Because VSCode in VirtualBox is a pain in the ass
docstring = '''
    Basic structure of the command set execution pool
    This is essentially the file/module loaded into a Class
        - All the stuff at the top level of the scope 
            - defs as thier name
            - variables as thier name
            - everything is considered an individual command 
              unless it matches a keyword like "steps"
                - Those commands are turned into Command() 's 
    
    
    '''
import sys
from pybashy.Command import Command
from pybashy.useful_functions import error_printer

class CommandSet():
    ''' metaclass'''
    def __init__(self,new_command_set_name):
        ''' waaat'''
        self.__dict__.update({'name':new_command_set_name})

class ModuleSet(CommandSet):  
    def __new__(cls):
        return super().__new__(cls)

    def __init__(self):
        self.name = str

    def __name__(self):
        return self.name

    def add_function(self, command_set : CommandSet):
        '''
    Assigns a CommandSet() Object to self for the purposes
    of having "functions" be thier own sets of commands

        - new attribute is named after CommandSet.name
        name is based on funciton name or command name
        '''
        self.__dict__.update({command_set.name : command_set})

    def add_command_dict(self, new_command_dict:dict):
        '''
        Names new attribute after command
        test_var = {'test1' : ['ls -la ~/','info','pass','fail']}
        CommandSet.add_command_dict(test_var)
        CommandSet.test1()

        '''
        try:
            new_command = Command()
            for command_name, command_container in new_command_dict.items():
                new_command.init_self({command_name : command_container})
                # assign Command() to Self
                setattr(self , new_command.name, new_command)
        # we kill it all here, the imported module didnt validate
        except Exception:
            error_printer('[-] Interpreter Message: CommandSet() Could not Init')  
            sys.exit()

class Function(CommandSet):
    def __init__(self):
        '''BLARP!'''