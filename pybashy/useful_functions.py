# -*- coding: utf-8 -*-
################################################################################
##                         pybashy - usefuf_functions.py                      ##
################################################################################
# Copyright (c) 2020 Adam Galindo                                             ##
#                                                                             ##
# Permission is hereby granted, free of charge, to any person obtaining a copy##
# of this software and associated documentation files (the "Software"),to deal##
# in the Software without restriction, including without limitation the rights##
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell   ##
# copies of the Software, and to permit persons to whom the Software is       ##
# furnished to do so, subject to the following conditions:                    ##
#                                                                             ##
# Licenced under GPLv3                                                        ##
# https://www.gnu.org/licenses/gpl-3.0.en.html                                ##
#                                                                             ##
# The above copyright notice and this permission notice shall be included in  ##
# all copies or substantial portions of the Software.                         ##
#                                                                             ##
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR  ##
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,    ##
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE ##
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER      ##
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,#
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN   ##
# THE SOFTWARE.                                                               ##
################################################################################
"""
BoilerPlate Galore!
 Here we have all the neat stuff you can just 
 import to add basic pro level functionality!

"""
__author__     = 'Adam Galindo'
__email__     = 'null@null.com'
__version__ = '1'
__license__ = 'GPLv3'

import sys
import logging
import threading
try:
    import colorama
    from colorama import init
    init()
    from colorama import Fore, Back, Style
    COLORMEQUALIFIED = True
except ImportError as derp:
    print("[-] NO COLOR PRINTING FUNCTIONS AVAILABLE")
    COLORMEQUALIFIED = False

blueprint   = lambda text: print(Fore.BLUE + ' ' +  text + ' ' + Style.RESET_ALL) if (COLORMEQUALIFIED == True) else print(text)
greenprint  = lambda text: print(Fore.GREEN + ' ' +  text + ' ' + Style.RESET_ALL) if (COLORMEQUALIFIED == True) else print(text)
redprint    = lambda text: print(Fore.RED + ' ' +  text + ' ' + Style.RESET_ALL) if (COLORMEQUALIFIED == True) else print(text)
# inline colorization for lambdas in a lambda
makered     = lambda text: Fore.RED + ' ' +  text + ' ' + Style.RESET_ALL if (COLORMEQUALIFIED == True) else None
makegreen   = lambda text: Fore.GREEN + ' ' +  text + ' ' + Style.RESET_ALL if (COLORMEQUALIFIED == True) else None
makeblue    = lambda text: Fore.BLUE + ' ' +  text + ' ' + Style.RESET_ALL if (COLORMEQUALIFIED == True) else None
makeyellow  = lambda text: Fore.YELLOW + ' ' +  text + ' ' + Style.RESET_ALL if (COLORMEQUALIFIED == True) else None
yellow_bold_print     = lambda text: print(Fore.YELLOW + Style.BRIGHT + ' {} '.format(text) + Style.RESET_ALL) if (COLORMEQUALIFIED == True) else print(text)

log_file = '/tmp/logtest'
logging.basicConfig(filename=log_file, format='%(asctime)s %(message)s', filemode='w')
logger                   = logging.getLogger()
logger.setLevel(logging.DEBUG)
debug_message        = lambda message: logger.debug(blueprint(message)) 
info_message        = lambda message: logger.info(greenprint(message)) 
warning_message     = lambda message: logger.warning(yellow_bold_print(message)) 
error_message        = lambda message: logger.error(redprint(message)) 
critical_message     = lambda message: logger.critical(yellow_bold_print(message))

def error_exit(self, message : str, derp : Exception):
    error_message(message = message)
    print(derp.with_traceback)
    sys.exit()

def threader(self, thread_function, name):
	try:
	    info_message("Thread {}: starting".format(name))
    	thread = threading.Thread(target=thread_function, args=(1,))
    	thread.start()
    	info_message("Thread {}: finishing".format(name))
	except Exception as derp:
        return derp
