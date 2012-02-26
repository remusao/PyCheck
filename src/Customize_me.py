################################################################################
#
#  PyCheck is a general purpose test_suit for project of any size.
#
#  Copyright (C) 2011-2012  Remi BERSON - Romain GUYOT DE LA HARDROUYERE
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################

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
         |___/                                  \n"



def prelude():
  """
    You can do here something that you want *before* everything starts
  """
  return



def epilog():
  """
    You can do here something that will be done after everything else
  """
  return



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


  def __str__(self):
    """
      Return a string that will be printed if we call :
        print some_test
      It's usefull to have a good output that could be printed in the
      fail_test summary
    """
    return '\n'.join(self.f,
                     'success')

  def __call__(self, info):
    """
      Your test will be exec this way, by calling it
      (eg : my_test (info)).
      Info is a dictionary that contains every options present
      in the info file, the command line or the config file.
    """
    self.info = info
    self.result = self._run()
    return self.result

  def _run(self):
    """
      ! Will be called by __call__
      Run the test, you can do anything you want but you must
      return True (if the tests has succeeded) of False (otherwise)
    """
    if random.randint(0, 1):
      return True
    else:
      return False


  def error_get(self):
    """
      In case of failure return an error message that will be printed in the output
      ! Warning : if you use colors (with \033[xxm command), the nb_col_mark var must
      contain the number of balises you used
    """
    message = "error"
    nb_col_mark = 0
    # (nb_col_mark, message)
    return (nb_col_mark, message)
