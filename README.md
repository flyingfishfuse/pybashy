# pybashy
	framework for leveraging python to run sets of shell commands for specific tasks. 

  
Only one set of commands can be at the top level of a file
  - Command Sets are stored as dicts in seperate files and loaded dynamically.
  - Multiple sets can be placed in thier own unique functions
  - functions MUST START with "function"
  - Classes not allowed as implied inheritance isnt working yet

you import modules with :

	new_command = CommandRunner()
	new_command.dynamic_import('commandtest')

to run the execution pool, you use the worker_bee() function:

	finished_command = new_command.worker_bee()

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
	  'test2' : ['ls -la ./','','','']
	}


Basic structure of an extension/script is as thus

    steps = { 'ls_user' : ["ls -la ~/", "[+] Command Sucessful", "[-]  Command Failed! Check the logfile!"],
		 'ls_root' : ["ls -la /", "[+] Command Sucessful!", "[-]  Command Failed! Check the logfile!"],
		 'ls_etc'  : ["ls -la /etc", "[+] Command Sucessful", "[-] ls -la Failed! Check the logfile!"]
        	}
    info_message = "[+] Informational Text!"
    success_message = "[+] Test Sucessful!"
    failure_message = "[-] Test Failure!"

    def function_test_function1(params):
      steps = { 'ls_user' : ["ls -la ~/", "[+] Command Sucessful", "[-]  Command Failed! Check the logfile!"],
		     'ls_root' : ["ls -la /", "[+] Command Sucessful!", "[-]  Command Failed! Check the logfile!"],
		     'ls_etc'  : ["ls -la /etc", "[+] Command Sucessful", "[-] ls -la Failed! Check the logfile!"]
			    }
	   info_message	= "[+] Informational Text!"
	   success_message = "[+] Test Sucessful!"
	   failure_message = "[-] Test Failure!"

Obvoiusly you can perform `str.format(thing)` on the commands, provided they are formatted properly for `os.popen()`
Thereby allowing you to perform complex shell scripting through a pythonic interface. I suggest you use bpython with it 
Until I manage to incorporate that environment
