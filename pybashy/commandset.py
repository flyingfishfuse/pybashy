basic_items = ['steps','success_message', 'failure_message', 'info_message']
#meta class for loading the command sets into
class CommandSet():
	'''
	Basic structure of the command set execution pool
	feed it kwargs
	then feed it to the STEPPER
	'''
	def __new__(cls, clsname, bases, clsdict):
		return super().__new__(cls, clsname, bases, clsdict)
		
	def error_exit(self, message : str, derp):
		#error_message(message = message)
		print(derp.with_traceback)
		#sys.exit()	
	
	def __init__(self, kwargs):
		self.steps = dict
		self.info_message	 = str
		self.success_message = str
		self.failure_message = str
		#attempt to assign everything
		#['steps','success_message', 'failure_message']
		try:
			for (key, value) in kwargs.items():
				if key in basic_items:
					setattr(self, key, value)
				elif key.startswith('function'):
					setattr(self, key, value)
				else:
					raise KeyError(str(key))
		except Exception as derp:
			self.error_exit('[-] CRITICAL ERROR: input file didnt validate, check your syntax maybe?', derp)
