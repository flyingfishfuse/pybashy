
import pybashy_monilithic
from pybashy_monilithic import *
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