docstring = '''
    This class hold each individual step
    It is the direct translation/representation of :
        {'test1' : ['ls -la ~/','','','']}

    This is the bottom of the container chain
     - ONE ExecutionPool() -> many CommandSet() -> many Command(command : dict)

    We use it as thus:
        command_dict = {'test1' : ['ls -la ~/','info','pass','fail']}
        new_command = Command()
        new_command.init_self(command_dict)
'''

from pybashy.internal_imports import error_printer,greenprint,CommandFormatException

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
