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

from test_tree import TestTree
from test import Test


class Build():
  """
    Will visit the TestTree to replace string that
    represent file_path by a Test object
  """

  def __call__(self, info):
    """
      Save the info file in an attribute and then
      parse subdirectories to build TestTree.
      Will call the _build_tests method and then
      return back the info dict with the Tree updated
    """
    self.info = info

    if 'TestTree' in self.info:
      self._build_tests(self.info['TestTree'])
    else:
      raise Exception("TestTree doesn't exists.")

    return self.info


  def _build_tests(self, tree):
    """
      1) Replace each test (the path as a String) by a Test object.
      2) Consolidate the testTree by updating the total number of test
        of each category
    """
    total = len(tree.tests)
    test_list = []

    for f in tree.tests:
      test_list.append(Test(tree.info, f, tree.cat))
    tree.tests = test_list

    for sub in tree.subcat:
      total += self._build_tests(sub)

    tree.total = total

    return total
