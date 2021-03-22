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

from pybashy.useful_functions import error_printer,greenprint

basic_items  = ['__name__', 'steps','success_message', 'failure_message', 'info_message']

class Command():
    def __new__(cls):
        cls.__name__ = str
        return super().__new__(cls)

    # These are for error checking
    def __init__(self):
        self.cmd_line           = str
        self.info_message       = str
        self.success_message    = str
        self.failure_message    = str
        self.name               = str

    def init_self(self,command: dict):
        try:
            for command_name, command_action_set in command.items():
                self.name            = command_name
                self.cmd_line        = command_action_set[0]
                self.info_message    = command_action_set[1]
                self.success_message = command_action_set[2]
                self.failure_message = command_action_set[3]
        except Exception:
            error_printer("[-] Instantiation of Command() Failed! One of these is not like the others!")

    def __repr__(self):
        greenprint("Command:")
        print(self.name)
        greenprint("Command String:")
        print(self.cmd_line)

    def __name__(self):
        return self.name
