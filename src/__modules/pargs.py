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



import argparse


class Parse_arg():
  """
    Argument parser task that will parse args and create the info dict
  """

  def __call__(self, info):
    """
      Parse arguments given to the test_suit program
    """
    self.info = info

    parser = argparse.ArgumentParser(description='Pycheck default')

    parser.add_argument('--version', action='version', version='Pycheck version 0.42')
    parser.add_argument('--pretty-print', nargs='+', default=['all'], metavar='categorie' ,help='Pretty-print the test tree')
    parser.add_argument('--graph', nargs='+', default=['all'], metavar='categorie' ,help='display graph at the end of tests')
    parser.add_argument('-c', nargs='+', default=['all'], metavar='categorie' ,help='Specifies the categories to test')

    return self.info
