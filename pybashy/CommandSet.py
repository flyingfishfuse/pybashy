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
from pybashy.Command import *

class CommandSet():
    def __new__(cls):
        cls.__name__ = str
        return super().__new__(cls)

    def __init__(self):
        # simply a list of the names
        # grab by iteration on Command.__name__
        pass

    def add_command_dict(self, name, new_command_dict:dict):
        '''
        {'test1' : ['ls -la ~/','info','pass','fail']}
        '''
        try:
            new_command = Command()
            for command_name, command_container in new_command_dict.items():
                new_command.init_self({command_name : command_container})
                # assign Command() to Self
                setattr(self , new_command.__name__, new_command)
        # we kill it all here, the imported module didnt validate
        except Exception:
            error_printer('[-] Interpreter Message: CommandSet() Could not Init')  
            sys.exit()
