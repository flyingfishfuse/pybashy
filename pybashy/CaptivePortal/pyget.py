#!/usr/bin/python3
# -*- coding: utf-8 -*-
################################################################################
##   Page Mirroring script utilizing python/Wget in a unix-like environment   ##
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
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
################################################################################
import os
import sys
import argparse
import requests
import subprocess


parser = argparse.ArgumentParser(description='page mirroring tool utilizing wget via python scripting')
parser.add_argument('--target',
                                 dest    = 'target',
                                 action  = "store" ,
                                 default = "127.0.0.1" ,
                                 help    = "Website to mirror, this is usually the only option you should wset. Multiple downloads \
                                            will be stored in thier own directories, ready for hosting internally. " )
parser.add_argument('--wgetopts',
                                 dest    = 'wgetopts',
                                 action  = "store" ,
                                 default = "-nd -H -np -k -p -E" ,
                                 help    = "Wget options, Mirroring to a subdirectory is the default" )
parser.add_argument('--user-agent',
                                 dest    = 'useragent',
                                 action  = "store" ,
                                 default = 'Mozilla/5.0 (X11; Linux x86_64; rv:28.0) Gecko/20100101  Firefox/28.0' ,
                                 help    = "User agent to bypass crappy limitations" )
parser.add_argument('--directory_prefix',
                                 dest    = 'directory_prefix',
                                 action  = "store" ,
                                 default = './website_mirrors/' ,
                                 help    = "Storage directory to place the downloaded files in, defaults to script working directory" )

class GetPage():
    """
    Class that performs the page mirroring, creating a subdirectory with all relevant files
    for display in a browser of your choice
    User agent might need tweaking

    :param: directory_prefix
        :type: string
    :param: target
        :type: list
    :param: useragent
        :type: string
    
    """
    def __init__(self, directory_prefix:string, target:list , useragent:string , wget_options:string):
        self.request_headers    = {'User-Agent' : useragent }
        self.storage_directory  = directory_prefix
        self.url_to_grab        = target
        self.wgetoptions        = wget_options
        # TODO: add user agent headers to prevent fuckery 
        self.wget_command  = {"wget" : ['wget {} --directory-prefix={}'.format(self.wgetoptions , self.storage_directory),
                                        "[+] Fetching Webpage",
                                        "[+] Page Downloaded",
                                        "[-] Download Failure"]
                            }
        self.grab(self.url_to_grab)

    def move_shell(self, directory = sys.argv[0]):
        #change shell to script directory by default
        os.chdir(os.path.dirname(directory))

    def grab(url:list):
        for each in url:
            page_downloader = DownloadPool(self.wget_command , each)

class DownloadPool():
    '''
    This is the download pool threading class for multiple website downloads
    
    Input : 
        :param: wget_command
            :type: dict
            - programmed/default flags ' -nd -H -np -k -p -E '
            - follows pybashy spec for output messaging

        :param: url 
            - Default '127.0.0.1'
    
    '''
    def __init__(self, wget_dict, website_to_download):
        self.script_cwd               = Path().absolute()
        self.script_osdir           = Path(__file__).parent.absolute()
        self.wget_dict          = wget_dict
        self.website_to_grab    = website_to_download
        self.step()
 
    def step(self):
        try:
            for instruction in self.wget_dict.values():
                self.current_command     = instruction[0]
                info                    = instruction[1]
                success                 = instruction[2]
                fail                     = instruction[3]
                yellow_bold_print(info)
                #### Deviation from pybasy core ####
                wget_cmd_exec  = GenPerp_threader(self.exec_command(self.current_command),new_thread_name)
                if wget_cmd_exec.returncode == 0 :
                #### End Deviation ####
                    info_message(success)
                else:
                    error_message(fail)
        except Exception as derp:
            return derp
            
    def error_exit(self, message : str, derp : Exception):
        error_message(message = message)
        print(derp.with_traceback)
        sys.exit()    


    def exec_command(self, command, blocking = True, shell_env = True):
        '''TODO: add formatting'''
        try:
            if blocking == True:
                step = subprocess.Popen(command,
                                        shell=shell_env,
                                         stdout=subprocess.PIPE,
                                         stderr=subprocess.PIPE)
                output, error = step.communicate()

                # output formatting can go here
                for output_line in output.decode().split('\n'):
                    info_message(output_line)
                # error formatting can go here
                for error_lines in error.decode().split('\n'):
                    critical_message(error_lines)
                return step

            # TODO: not implemented yet
            elif blocking == False:
                # TODO: not implemented yet
                pass

        except Exception as derp:
            yellow_bold_print("[-] Shell Command failed!")
            return derp
    
class GenPerp_threader():
    '''
    General Purpose threading implementation that accepts a generic programmatic entity
    '''
    def __init__(self,function_to_thread):
        self.thread_function = function_to_thread
        self.function_name   = getattr(self.thread_function.__name__)

    def threader(self, thread_function, name):
        info_message("Thread {}: starting".format(self.function_name))
        thread = threading.Thread(target=self.thread_function, self.function_name)
        thread.start()
        info_message("Thread {}: finishing".format(name))

if __name__ == "__main__":
    arguments  = parser.parse_args()
    wget_thing = GetPage(arguments.directory_prefix,
                         arguments.target,
                         arguments.useragent,
                         arguments.wget_options)