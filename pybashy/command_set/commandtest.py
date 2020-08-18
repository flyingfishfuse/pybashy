# -*- coding: utf-8 -*-
################################################################################
##			pybash, a tool for using linux commands with python				  ##
################################################################################
# Copyright (c) 2020 Adam Galindo											  ##
#																			  ##
# Permission is hereby granted, free of charge, to any person obtaining a copy##
# of this software and associated documentation files (the "Software"),to deal##
# in the Software without restriction, including without limitation the rights##
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell   ##
# copies of the Software, and to permit persons to whom the Software is		  ##
# furnished to do so, subject to the following conditions:					  ##
#																			  ##
# Licenced under GPLv3														  ##
# https://www.gnu.org/licenses/gpl-3.0.en.html								  ##
#																			  ##
# The above copyright notice and this permission notice shall be included in  ##
# all copies or substantial portions of the Software.						  ##
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
####
################################################################################

"""
This is a most basic example of the command framework

	- you import this file with :
		
		new_command = CommandRunner()
		new_command.dynamic_import('commandtest')

	- to run the execution pool, you use the worker_bee() function:

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
		'test2' : ['ls -la ~/','','','']
	}



"""
__author__ = 'Adam Galindo'
__email__ = 'null@null.com'
__version__ = '1'
__license__ = 'GPLv3'

# only one set like this allowed
steps = { 'ls_user' : ["ls -la ~/", "[+] Info Text",
									"[+] Command Sucessful", 
									"[-] Command Failed! Check the logfile!"],
		  'ls_root' : ["ls -la /",	"[+] Info Text",
		  							"[+] Command Sucessful!", 
									"[-] Command Failed! Check the logfile!"],
		  'ls_etc'  : ["ls -la /etc","[+] Info Text",
		  							"[+] Command Sucessful", 
									"[-] ls -la Failed! Check the logfile!"]
			}
info_message	= "[+] Informational Text!"
success_message = "[+] Test Sucessful!"
failure_message = "[-] Test Failure!"


#multiple sets like this allowed
packages = 'lolcat'
apt_install = { 
				'test1': ["sudo apt install {}".format(packages),
								'Informational Text!',
								"[+]Sucessful!",
								"[-]Failure!"]
				}

test1 = {'test1' : ['ls -la ~/','info','pass','fail']}
# functions MUST START with "function"
# many of these allowed
def function_test_function1(params):
	steps = { 
				'ls_user' : ["ls -la ~/", 	"[+] Info Text",
											"[+] Command Sucessful", 
											"[-] Command Failed! Check the logfile!"],
			   'ls_root' : ["ls -la /",		"[+] Info Text",
			   								"[+] Command Sucessful!", 
											"[-] Command Failed! Check the logfile!"],
			   'ls_etc'  : ["ls -la /etc",	"[+] Info Text",
			   								"[+] Command Sucessful", 
											"[-] ls -la Failed! Check the logfile!"]
			}
	info_message	= "[+] Informational Text!"
	success_message = "[+] Test Sucessful!"
	failure_message = "[-] Test Failure!"

def function_test_function2(params):
	steps = { 
				'ls_user' : ["ls -la ~/", "[+] Info Text",
										"[+] Command Sucessful", 
										"[-] Command Failed! Check the logfile!"],
			   'ls_root' : ["ls -la /", "[+] Info Text",
			   							"[+] Command Sucessful!",
										"[-] Command Failed! Check the logfile!"],
			   'ls_etc'  : ["ls -la /etc","[+] Info Text",
			   							"[+] Command Sucessful",
										"[-] ls -la Failed! Check the logfile!"]
			}
	info_message	= "[+] Informational Text!"
	success_message = "[+] Test Sucessful!"
	failure_message = "[-] Test Failure!"
	