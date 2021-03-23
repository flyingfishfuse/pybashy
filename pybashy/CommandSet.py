import sys
from pybashy.Command import Command
from pybashy.useful_functions import error_printer

class CommandSet():
    ''' metaclass'''
    def __init__(self,new_command_set_name):
        ''' waaat'''
        self.name = new_command_set_name

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
    '''
        This is essentially the file/module loaded into a Class
    '''
    def __new__(cls):
        return super().__new__(cls)

    def __init__(self):
        self.name = str

    def __name__(self):
        return self.name


class Function(CommandSet):
    ''' individual functions fit here'''
    def __init__(self):
        '''BLARP!'''