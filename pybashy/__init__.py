#blarp!

#TODO: Do something with this to get, set, the environment for pybashy to run properly
class CustomException(Exception):
    '''Base Class for Internal Exception Labeling'''

class CommandFormatException(CustomException):
    '''Failure in the text of a Command(command_input)
    An internal Error unless you are feeding JSON directly
    to:
        - Command.init_self(json_str : json)'''
    def __init__(self, derp:str, errors):
        ''' narf!'''