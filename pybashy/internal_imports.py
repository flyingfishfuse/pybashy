#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
This file contains: 
    - Useful bits of code I use in all my projects

"""
__author__  = 'Adam Galindo'
__email__   = 'null@null.com'
__version__ = '0.1A'
__license__ = 'GPLv3'

#currently controls color printing functions ONLY
TESTING = True

########################################
# Imports for logging and colorization #
########################################
import sys
import os,pkgutil
import argparse
import logging
import traceback

try:
    import colorama
    from colorama import init
    init()
    from colorama import Fore, Back, Style
    if TESTING == True:
        COLORMEQUALIFIED = True
except ImportError as derp:
    print("[-] NO COLOR PRINTING FUNCTIONS AVAILABLE, Install the Colorama Package from pip")
    COLORMEQUALIFIED = False

####################################################################################
# Commandline Arguments
###################################################################################
# If the user is running the program as a script we parse the arguments or use the 
# config file. 
# If the user is importing this as a module for usage as a command framework we do
# not activate the argument or configuration file parsing engines
parser = argparse.ArgumentParser(description='python based, bash task execution manager')

parser.add_argument('--testing',
                             dest    = 'testing',
                             action  = "store_true" ,
                             help    = 'will run a series of tests, testing modules not supported yet' )
parser.add_argument('--use-config',
                             dest    = 'config_file',
                             action  = "store_true" ,
                             help    = 'Use config file, if used, will ignore other options' )
parser.add_argument('--config-filename',
                             dest    = 'config_filename',
                             action  = "store" ,
                             help    = 'Name of the config file' )
parser.add_argument('--execute-module',
                             dest    = 'dynamic_import',
                             action  = "store_true" ,
                             help    = 'Will execute user created module if used, will ignore config options ' )
parser.add_argument('--module-name',
                             dest    = 'dynamic_import_name',
                             action  = "store" ,
                             help    = 'Name of module to load' )

##########################
# Colorization Functions #
##########################
# yeah, about the slashes... do you want invisible \n? 
# Because thats how you avoid invisible \n and concatenation errors
blueprint             = lambda text: print(Fore.BLUE + ' ' +  text + ' ' + \
    Style.RESET_ALL) if (COLORMEQUALIFIED == True) else print(text)
greenprint             = lambda text: print(Fore.GREEN + ' ' +  text + ' ' + \
    Style.RESET_ALL) if (COLORMEQUALIFIED == True) else print(text)
redprint             = lambda text: print(Fore.RED + ' ' +  text + ' ' + \
    Style.RESET_ALL) if (COLORMEQUALIFIED == True) else print(text)
# inline colorization for lambdas in a lambda
# lambing while you lamb?
makered                = lambda text: Fore.RED + ' ' +  text + ' ' + \
    Style.RESET_ALL if (COLORMEQUALIFIED == True) else None
makegreen              = lambda text: Fore.GREEN + ' ' +  text + ' ' + \
    Style.RESET_ALL if (COLORMEQUALIFIED == True) else None
makeblue              = lambda text: Fore.BLUE + ' ' +  text + ' ' + \
    Style.RESET_ALL if (COLORMEQUALIFIED == True) else None
makeyellow             = lambda text: Fore.YELLOW + ' ' +  text + ' ' + \
    Style.RESET_ALL if (COLORMEQUALIFIED == True) else None
yellow_bold_print     = lambda text: print(Fore.YELLOW + Style.BRIGHT + \
    ' {} '.format(text) + Style.RESET_ALL) if (COLORMEQUALIFIED == True) else print(text)

###########
# LOGGING #
###########
LOGLEVEL = 'DEV_IS_DUMB'
LOGLEVELS = [1,2,3,'DEV_IS_DUMB']

log_file  = 'garden_grid_message_log'
logging.basicConfig(filename=log_file, format='%(asctime)s %(message)s', filemode='w')
logger    = logging.getLogger()


debug_message = lambda message: logger.debug(blueprint(message)) 
info_message  = lambda message: logger.info(greenprint(message))   
warning_message  = lambda message: logger.warning(yellow_bold_print(message)) 
error_message    = lambda message: logger.error(redprint(message)) 
critical_message = lambda message: logger.critical(yellow_bold_print(message))

def error_printer(message):
    exc_type, exc_value, exc_tb = sys.exc_info()
    trace = traceback.TracebackException(exc_type, exc_value, exc_tb) 
    if LOGLEVEL == 'DEV_IS_DUMB':
        error_message( message + ''.join(trace.format_exception_only()))
        try:
            traceback.format_list(traceback.extract_tb(trace)[-1:])[-1]
        except Exception:
            error_message(trace.exc_traceback.tb_frame.f_code)
        debug_message('LINE NUMBER >>>' + str(exc_tb.tb_lineno))
    else:
        error_message(message + ''.join(trace.format_exception_only()))

def list_modules():
    '''
Lists modules in command_set directory
    '''
    list_of_modules = []
    command_files_dir = os.path.dirname(__file__) + "/commandset"        
    list_of_subfiles  = pkgutil.iter_modules([command_files_dir])
    for filez in list_of_subfiles:
        print(filez.name)
        list_of_modules.append(filez.name)
    return list_of_modules

class CustomException(Exception):
    '''Base Class for Internal Exception Labeling'''

class CommandFormatException(CustomException):
    '''Failure in the text of a Command(command_input)
    An internal Error unless you are feeding JSON directly
    to:
        - Command.init_self(json_str : json)'''
    def __init__(self, derp:str, errors):
        exc_type, exc_value, exc_tb = sys.exc_info()
        trace = traceback.TracebackException(exc_type, exc_value, exc_tb) 
        if LOGLEVEL == 'DEV_IS_DUMB':
            error_message( derp + ''.join(trace.format_exception_only()))
            critical_message(errors)
            try:
                traceback.format_list(traceback.extract_tb(trace)[-1:])[-1]
            except Exception:
                error_message(trace.exc_traceback.tb_frame.f_code)
            debug_message('LINE NUMBER >>>' + str(exc_tb.tb_lineno))
        else:
            error_message(derp + ''.join(trace.format_exception_only()))

###############################################

## BeautifulSoup4 
#divs = soupyresults.find(lambda tag:  tag.name=='div' and tag.has_key('id') and tag['id'] == divname)

################################################]
## SQLALCHEMY
#################################################
wat = '''
def check_if_plants_exist_bool(plant_name):
    exists = PlantDatabase.session.query(Plants.id).filter_by(name=plant_name).first() is not None
    if exists:
        info_message()
        return True
    else:
        return False
        #hwhat the he-hockey stick hockey stick am I doing!?!?!?

'''
HWAT = '''
def table_exists(engine,name):
    try:
        from sqlalchemy import inspect
        blarf = inspect(engine).dialect.has_table(engine.connect(),name)
        print('[+] Database Table {} EXISTS'.format(name, blarf))
        #return blarf
    except Exception:
        error_printer("[-] TABLE {} does NOT EXIST!".format(name))
'''
