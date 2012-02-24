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


class TestTree():
  """
    A node of the tree that contains the tests
    Description of the attributes :
      - cat : name of the category
      - prefix : absolute prefix of this category
      - level : depth of the category's directory (0 is the root)
      - info : Content of the info file
      - tests : list of the tests present in the category
      - subcat : list of the subcategories

      - total : total number of tests
      - success : number of success
      - fail : number of fails
  """

  def __init__(self, level, prefix, cat):
    """
    """
    self.cat = cat
    self.prefix = prefix
    self.level = level
    self.info = {}
    self.tests = []
    self.subcat = []

    self.total = 0
    self.success = 0
    self.fail = 0



  def pretty_print(self):
    """
    """
    space = ' ' * (self.level * 4)
    print space, 'category :', self.cat
    print space, 'prefix :', self.prefix
    print space, 'level :', self.level
    print space, 'info :', self.info
    print space, 'total :', self.total, ' | success :', self.success, \
                 ' | fail :', self.fail
    print space, '--------------------'
    for cat in self.subcat:
      cat.pretty_print()
