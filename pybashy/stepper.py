import subprocess
from pathlib import Path
from pybash.useful_functions import info_message,error_message,yellow_bold_print,critical_message

class Stepper:
#getattr, setattr and self.__dict__
	'''
Steps through the command list
	'''
	def __init__(self):
		self.script_cwd		   	= Path().absolute()
		self.script_osdir	   	= Path(__file__).parent.absolute()
		self.example  = {"ls_root"  : ["ls -la /", "[+] success message", "[-] failure message" ]}
		self.example2 = {"ls_etc"  : ["ls -la /etc"		  , "[-] failure message", "[+] success message" ] ,
		 	 			 "ls_home" : ["ls -la ~/", "[-] failure message", "[+] success message" ] ,}
	
	def step_test(self, dict_of_commands : dict):
		'''
	edit this and propogate changes to self.step() to reflect changes in 
	modules
		'''
		try:
			for instruction in self.example.values(), self.example2.values():
				cmd 	= instruction[0]
				success = instruction[1]
				fail 	= instruction[2]
				self.current_command = cmd
				stepper = self.exec_command(str(self.current_command))
				if stepper.returncode == 1 :
					info_message(success)
				else:
					error_message(fail)
		except Exception as derp:
			return derp

	def step(self, dict_of_commands : dict):
		try:
			for instruction in dict_of_commands.values():
				cmd 	= instruction[0]
				success = instruction[1]
				fail 	= instruction[2]
				self.current_command = cmd
				stepper = self.exec_command(self.current_command)
				if stepper.returncode == 0 :
					info_message(success)
				else:
					error_message(fail)
		except Exception as derp:
			return derp
	
	def exec_command(self, command, blocking = True, shell_env = True):
		'''TODO: add formatting'''
		#read, write = os.pipe()
#		step = subprocess.Popen(something_to_set_env, 
#						shell=shell_env, 
#						stdin=read, 
#						stdout=sys.stdout, 
#						stderr=subprocess.PIPE)
#		Note that this is limited to sending a maximum of 64kB at a time,
# 		pretty much an interactive session
#		byteswritten = os.write(write, str(command))

		try:
			if blocking == True:
				step = subprocess.Popen(command,
										shell=shell_env,
				 						stdout=subprocess.PIPE,
				 						stderr=subprocess.PIPE)
				output, error = step.communicate()
				for output_line in output.decode().split('\n'):
					info_message(output_line)
				for error_lines in error.decode().split('\n'):
					critical_message(error_lines)
				return step
			elif blocking == False:
				# TODO: not implemented yet				
				pass
		except Exception as derp:
			yellow_bold_print("[-] Shell Command failed!")
			return derp
	
	def worker_bee(self, flower , pollen):
		'''
	Worker_bee() gathers up all the things to do and brings them to the stepper
	Dont run this function unless you want to run the scripts!
	
		- Flower is a CommandSet() and is Required
		
		- Pollen is the name of the function to run!
			only required if running in scripting mode
		'''
		try:
			#requesting a specific function
			if pollen == True:
				#filter out class stuff, we are searching for functions
				for thing in dir(flower):
					if thing.startswith('function') and thing.endswith(pollen):
						self.success_message = getattr(thing,'success_message')
						self.failure_message = getattr(thing,'failure_message')
						self.steps			 = getattr(thing,'steps')
						stepper = self.step(self.steps)
						if isinstance(stepper, Exception):
							self.error_exit(self.failure_message, Exception)
						else:
							print(self.success_message)
			# the user wants to run all functions in the class
			else:
				for thing in dir(flower:)
					if thing.startswith('__') != True:
						#if we imported a function, assign things properly
						if thing.startswith('function'):
							print(thing)
							self.success_message = getattr(thing,'success_message')
							self.failure_message = getattr(thing,'failure_message')
							self.info_message    = getattr(thing,'failure_message')
							self.steps			 = getattr(thing,'steps')
							stepper = self.step(self.steps)
							if isinstance(stepper, Exception):
								self.error_exit(self.failure_message, Exception)
							else:
								print(self.success_message)
			# otherwise, everything is already assigned
			stepper = self.step(self.steps)
			if isinstance(stepper, Exception):
				self.error_exit(self.failure_message, Exception)
			else:
				print(self.success_message)

	def error_exit(self, message : str, derp : Exception):
		error_message(message = message)
		print(derp.with_traceback)
		#sys.exit()