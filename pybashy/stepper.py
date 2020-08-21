
import sys
import subprocess
from pathlib import Path
from pybashy.commandset import ExecutionPool
from pybashy.useful_functions import info_message,error_message,yellow_bold_print,critical_message

class Stepper:
#getattr, setattr and self.__dict__
	'''
Steps through the command list
	'''
	def __init__(self):
		self.script_cwd		   	= Path().absolute()
		self.script_osdir	   	= Path(__file__).parent.absolute()
		self.example  = {"ls_root" : ["ls -la /", "info", "[+] success message", "[-] failure message" ]}
		self.example2 = {"ls_etc"  : ["ls -la /etc"	,'info', "[-] failure message", "[+] success message" ] ,
		 	 			 "ls_home" : ["ls -la ~/", 'info', "[-] failure message", "[+] success message" ]}


	def error_exit(self, message : str, derp : Exception):
		error_message(message = message)
		print(derp.with_traceback)
		sys.exit()	
	
	def step_test(self, dict_of_commands : dict):
		'''
	edit this and propogate changes to self.step() to reflect changes in 
	modules
		'''
		try:
			for instruction in self.example.values(), self.example2.values():
				cmd 	= instruction[0]
				info    = instruction[1]
				success = instruction[2]
				fail 	= instruction[3]
				self.current_command = cmd
				exec_pool = ExecutionPool()
				exec_pool.exec_command(self.current_command)
				if exec_pool.returncode == 1 :
					info_message(success)
				else:
					error_message(fail)
		except Exception as derp:
			return derp

	def step(self, dict_of_commands : dict):
		try:
			for instruction in dict_of_commands.values():
				cmd 	= instruction[0]
				info    = instruction[1]
				success = instruction[2]
				fail 	= instruction[3]
				yellow_bold_print(info)
				self.current_command = cmd
				exec_pool = ExecutionPool()
				exec_pool.exec_command(self.current_command)
				if exec_pool.returncode == 0 :
					info_message(success)
				else:
					error_message(fail)
		except Exception as derp:
			return derp
	
	def worker_bee(self, flower , pollen = ''):
		'''
	Worker_bee() gathers up all the things to do and brings them to the stepper
	Dont run this function unless you want to run the scripts!
	
		- Flower is a CommandSet() and is Required
		
		- Pollen is the name of the function to run!
			only required if running in scripting mode
		'''
		try:
			#requesting a specific function_function
			if pollen != '':
				#filter out class stuff, we are searching for functions
				for thing in dir(flower):
					if thing.startswith('function') and thing.endswith(pollen):
						self.success_message = getattr(thing,'success_message')
						self.failure_message = getattr(thing,'failure_message')
						self.info_message	 = getattr(thing,'info_message')
						self.steps			 = getattr(thing,'steps')
						stepper = self.step(self.steps)
						if isinstance(stepper, Exception):
							self.error_exit(self.failure_message, Exception)
						else:
							print(self.success_message)
			# the user wants to run all functions in the class
			else:
				for thing in dir(flower):
					if thing.startswith('__') != True:
						#if we imported a function, assign things properly
						if thing.startswith('function'):
							print(thing)
							self.success_message = getattr(thing,'success_message')
							self.failure_message = getattr(thing,'failure_message')
							self.info_message	 = getattr(thing,'info_message')
							self.steps			 = getattr(thing,'steps')
							stepper = self.step(self.steps)
							if isinstance(stepper, Exception):
								self.error_exit(self.failure_message, Exception)
							else:
								print(self.success_message)
			# otherwise, everything is already assigned
			stepper = self.step(self.steps)
			if isinstance(stepper, Exception):
				print(stepper.error_message)
				raise stepper
			else:
				print(stepper.success_message)
		except Exception as derp:
			self.error_exit(self.failure_message, derp)