basic_items = ['steps','success_message', 'failure_message', 'info_message']
#meta class for loading the command sets into
class ExecutionPool():
	def __init__(self):
		pass

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

class Command:
	def __init__(self,command):
		self.command = dict

class CommandSet():
	'''
	Basic structure of the command set execution pool
	feed it kwargs
	then feed it to the STEPPER
	'''
	#def __new__(cls, clsname, bases, clsdict):
	#	return super().__new__(cls, clsname, bases, clsdict)
		
	def error_exit(self, message : str, derp):
		#error_message(message = message)
		print(derp.with_traceback)
		#sys.exit()	
	
	def __init__(self,kwargs):
		try:
			for (key, value) in kwargs.items():
				#if key in basic_items or (key.startswith('function')):
				setattr(self, key, value)
					#else:
						#raise KeyError(str(key))
		except Exception as derp:
			self.error_exit('[-] CRITICAL ERROR: input file didnt validate, check your syntax maybe?', derp)

	def run_command(command):
		for key, value in self.steps.items():
			if key == command:
				Command(command)
