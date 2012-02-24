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


from Customize_me import Test
from test_tree import TestTree
from display import *


class Run():
  """
    Task that will parse the TestTree and then run each test.
    - If the test succeeds, print a succeed output on STDOUT
    - If the test fails, print a fail output on STDOUT
    At the end, print a summary of the tests in a htop-like way
  """

  def __call__(self, info):
    """
      Save the info dict, call _run_tests on the root of
      the TestTree and then print the summary.
    """
    self.info = info
    self._run_tests(info['TestTree'])
    printResult(info['TestTree'])

    return self.info


  def _run_tests(self, tree):
    """
      Exec the tests recurcively on each category
    """
    printHeader(tree.cat, tree.level)
    tree.total = len(tree.tests)
    success, fail = 0, 0

    for test in tree.tests:
      res = test.run()
      if res:
        tree.success += 1
        printSuccess(test.f)
      else:
        tree.success += 1
        printFail(test.f, test.error_get())

    for sub in tree.subcat:
      tmp_succ, tmp_fail = self._run_tests(sub)
      success += tmp_succ
      fail += tmp_fail

    return success, fail
