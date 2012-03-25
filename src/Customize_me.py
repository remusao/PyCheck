###############################################################################
#                                                                             #
#    This file is part of the PyCheck project
#                                                                             #
#    Copyright (C) 2011-2012  Remi BERSON - Romain GUYOT DE LA HARDROUYERE    #
#                                                                             # 
#    This program is free software: you can redistribute it and/or modify     #
#    it under the terms of the GNU General Public License as published by     #
#    the Free Software Foundation, either version 3 of the License, or        #
#    (at your option) any later version.                                      #
#                                                                             #
#    This program is distributed in the hope that it will be useful,          #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of           #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the            #
#    GNU General Public License for more details.                             #
#                                                                             #
#    You should have received a copy of the GNU General Public License        #
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.    #
#                                                                             #
###############################################################################

import os, signal, time
import random


def logo_print():
  """
    If you want to print a logo when the test_suit is runned
  """

print "\n\
   ______      _____ _               _          \n\
   | ___ \    /  __ \ |             | |         \n\
   | |_/ /   _| /  \/ |__   ___  ___| | __      \n\
   |  __/ | | | |   | '_ \ / _ \/ __| |/ /      \n\
   | |  | |_| | \__/\ | | |  __/ (__|   <       \n\
   \_|   \__, |\____/_| |_|\___|\___|_|\_\      \n\
          __/ |                                 \n\
         |___/                                  \n\n\
  Version 0.2"



def prelude():
  """
    You can do here something that you want *before* everything starts
  """

  ##### FIXME ####

  pass

  #### END OF FIX ###


def prelude_cat(info):
  """
    This function will be called in every directory, before testing
  """

  ##### FIXME #####

  pass

  ##### END OF FIX ####



def epilog_cat():
  """
    This function will be called in every directory, after testing
  """

  ##### FIXME #####

  pass

  ##### END OF FIX ####



def epilog():
  """
    You can do here something that will be done after everything else
  """

  #### FIX ME ####

  pass

  #### END OF FIX ####


#
#
#    THE TEST OBJECT
#
#


class Test:
  """
    The class you must customize to do the tests you want on each file
  """

  def __init__(self, prefix, f):
    """
      prefix : contains the absolute prefix of the file (eg : /home/...)
      f : name of the file that contains the test
      category : name of the category
    """
    self.prefix = prefix
    self.f = f
    self.result = False

  #############################################################################
  #        ____ _  _ ____ ___ ____ _  _ _  ___  ____    ___ _  _ _ ____       #
  #        |    |  | [__   |  |  | |\/| | [___  |___     |  |__| | [__        #
  #        |___ |__| ___]  |  |__| |  | | ___]  |___     |  |  | | ___]       #
  #                                                                           #
  #                        ___  ____ ____ ___                                 #
  #                        |__] |__| |__/  |                                  #
  #                        |    |  | |  \  |                                  #
  #                                                                           #
  #############################################################################


  def __str__(self):
    """
      Return a string that will be printed if we call :
        print some_test
      It's usefull to have a good output that could be printed in the
      fail_test summary
    """

    #### FIX ME ###

    return '\n'.join(self.f, 'success')

    #### END OF FIX


  def __call__(self, info):
    """
      Your test will be exec this way, by calling it
      (eg : my_test (info)).
      Info is a dictionary that contains every options present
      in the info file, the command line or the config file.
    """

    #### FIX ME ####

    self.info = info
    self.result = self._run()
    return self.result

    #### END OF FIX ####


  def _run(self):
    """
      TIMEOUT : If you want to check timeout on subprocess, use the
      method self.timeout_wait(process, timeout) where process is your
      subprocess object and timeout is ine seconds

      ! Will be called by __call__
      Run the test, you can do anything you want but you must
      return True (if the tests has succeeded) of False (otherwise)
    """

    #### FIX ME ####

    if random.randint(0, 1):
      return True
    else:
      return False

    #### END OF FIX ####


  def error_get(self):
    """
      In case of failure return a *ONE-LINE* error message that will be printed
      in the output
      ! Warning : if you use colors (with \033[xxm command), the nb_col_mark var must
      contain the number of balises you used
    """

    #### FIX ME ####

    message = "error"
    nb_col_mark = 0
    # (nb_col_mark, message)
    return (nb_col_mark, message)

    #### END OF FIX ####


  def sumup_print(self):
    """
      This method will be called to display a summary of tests that failed.
      You could for exemple print a description of the test, error message,
      and in case of a subprocess invocation, a return code, a stdout and
      stderr.
    """

    #### FIX ME ####

    print "Description : 42"
    print "returned 2 instead of 0"
    print "Stderr : error number 1337"
    print "Stdout : I decided to crash !"

    #### END OF FIX ####


  #############################################################################
  #                           ____ _  _ ___     ____ ____                     #
  #                           |___ |\ | |  \    |  | |___                     #
  #                           |___ | \| |__/    |__| |                        #
  #                                                                           #
  #             ____ _  _ ____ ___ ____ _  _ _ ____ ____ ___ _ ____ _  _      #
  #             |    |  | [__   |  |  | |\/| | [__  |__|  |  | |  | |\ |      #
  #             |___ |__| ___]  |  |__| |  | | ___] |  |  |  | |__| | \|      #
  #                                                                           #
  #############################################################################


  def _kill_process(self, process):
    """
      Kill the process given as argument
    """
    try:
      os.kill(process.pid, signal.SIGTERM)
      if self.timeout_wait(process, 1) is not None:
        os.kill(process.pid, signal.SIGKILL)
    except OSError:
      pass


  def timeout_wait(self, process, timeout = 0):
    """
      wait for the given process to terminate.
      If timeout (in seconds), kill the process
    """
    if timeout is 0:
      if 'timeout' in self.info:
        timeout = self.info['timeout']
      else:
        timeout = 3
    t0 = time.time()
    delay = min(0.1, timeout)
    while True:
      time.sleep(delay)
      returncode = process.poll()
      if returncode is not None:
        return returncode
      tnow = time.time()
      if (tnow - t0) >= timeout:
        self._kill_process(process)
        return -1
      delay = min(delay * 2, timeout)
