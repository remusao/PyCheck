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


class Test:
  """
    The class you must customize to do the tests you want on each file
  """

  def __init__(self, info, f, category):
    """
      info : dictionary that contains every option present either in the info
        file in the directory of this test or in de command-line options.
      f : name of the file that contains the test
      category : name of the category
    """
    self.info = info
    self.f = f
    self.category = category
    self.result = True


  def __str__(self):
    """
      Return a string that will be printed if we call :
        print some_test
      It's usefull to have a good output that could be printed in the
      fail_test summary
    """
    return '\n'.join(self.f,
                     self.category,
                     'success')


  def run(self):
    """
      1) Run the test, you can do anything you want but you must
      return True (if the tests has succeeded) of False (otherwise)
      2) You must write this value in the self.result attribute
    """
    self.result = False
    return True


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
