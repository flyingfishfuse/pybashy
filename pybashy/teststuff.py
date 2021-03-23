cmdstrjson = {'ls_etc' : {"command" : "ls -la /etc" , "info_message": "[+] Info Text", "success_message" : "[+] Command Sucessful", "failure_message" : "[-] ls -la Failed! Check the logfile!"}}
class CommandSet():
    def __init__(self,new_command_set_name):
        self.__dict__.update({'name':new_command_set_name})
    def __name__(self):
        return self.name


    def add_function(self, command_set : CommandSet):
        cmd_name = command_set.__name__
        self.__dict__.update( { cmd_name : command_set } )

class Function(CommandSet):
    def __init__(self):
        '''BLARP!'''
    
new_command_set    = CommandSet()
new_function       = Function()
for command in cmdstrjson.keys:
    new_attr_name  = command
    new_attr_value = cmdstrjson.get(command)
    new_function.__dict__.update({new_attr_name : new_attr_value})