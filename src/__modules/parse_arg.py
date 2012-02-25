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

  def _maj_info(self, args):
    """
      Update the info dict with the arguments given on the command line
    """
    # Update the other argument
    for o in args['other']:
      tmp = o.split('=')
      if len(tmp) > 1:
        self.info[tmp[0]] = tmp[1]
      else:
        self.info[tmp[0]] = None

    del args['other']
    for arg in args:
      self.info[arg] = args[arg]



  def __call__(self, info):
    """
      Parse arguments given to the test_suit program
    """
    self.info = info

    parser = argparse.ArgumentParser(description='Pycheck default')

    parser.add_argument('--version', action='version', version='Pycheck version 0.42')
    parser.add_argument('-p', '--prettyprint', action='store_true',                       \
        help='Pretty print the TestTree')
    parser.add_argument('-t', '--timeout', type=int, default=info['timeout'],             \
        help='When running tests, check if the tests timeout, abort then in that case')
    parser.add_argument('-m', '--memcheck', default=info['memcheck'], action='store_true',\
        help='When running tests, look for memory leaks')
    parser.add_argument('-c', '--categories', nargs='+', default=['all'],                 \
        metavar='Category' ,help='Specifies the categories to test')
    parser.add_argument('-nv', '--noverbose', dest='verbose', default=info['verbose'],    \
        action='store_false',                                                             \
        help='Specifies a non-verbose ouput. By default the output is verbose.')
    parser.add_argument('-o', '--output', nargs='+', default=info['output'],              \
        metavar='file_format',                                                            \
        help='Output result in a specific format (latex, html, picture, etc..)')
    parser.add_argument('--other', nargs='+', metavar='custom_arg',                       \
        default=info['output'], help='Allow the user to specify custom arguments of the   \
        form args1=something1 arg2=something2')

    args = vars(parser.parse_args())
    self._maj_info(args)
    del args

    return self.info
