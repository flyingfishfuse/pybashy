# pybashy
	framework for leveraging python to run sets of shell commands for specific tasks. 

  
Only one set of commands can be at the top level of a file
  - Command Sets are stored as dicts in seperate files and loaded dynamically.
  - Multiple sets can be placed in thier own unique functions
  - functions MUST START with "function"
  - Classes not allowed as implied inheritance isnt working yet

Basic structure of an extension/script is as thus

    steps = { 'ls_user' : ["ls -la ~/", "[+] Command Sucessful", "[-]  Command Failed! Check the logfile!"],
		 'ls_root' : ["ls -la /", "[+] Command Sucessful!", "[-]  Command Failed! Check the logfile!"],
		 'ls_etc'  : ["ls -la /etc", "[+] Command Sucessful", "[-] ls -la Failed! Check the logfile!"]
        	}
    success_message = "[+] Test Sucessful!"
    failure_message = "[-] Test Failure!"

    def function_test_function1(params):
      steps = { 'ls_user' : ["ls -la ~/", "[+] Command Sucessful", "[-]  Command Failed! Check the logfile!"],
		     'ls_root' : ["ls -la /", "[+] Command Sucessful!", "[-]  Command Failed! Check the logfile!"],
		     'ls_etc'  : ["ls -la /etc", "[+] Command Sucessful", "[-] ls -la Failed! Check the logfile!"]
			    }
	   success_message = "[+] Test Sucessful!"
	   failure_message = "[-] Test Failure!"

Obvoiusly you can perform `str.format(thing)` on the commands, provided they are formatted properly for `os.popen()`
Thereby allowing you to perform complex shell scripting through a pythonic interface. I suggest you use bpython with it 
Until I manage to incorporate that environment
