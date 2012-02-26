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


import sys, os 
from Customize_me import Test
from test_tree import TestTree


class Build():
  """
    Module that will parse the subdirectories to find all tests files and build
    a TestTree with them
  """

  def __call__(self, info):
    """
      Save the dic info and call _gen_tree.
      The resulting tree is then stored in the
      info dic with the key 'TestTree'
    """
    self.info = info
    root = TestTree(0, '', 'Total')
    total = 0

    for path in self.info['test_path']:
      for f in os.listdir(path):
        if os.path.isdir(f):
          os.chdir(f)
          root.subcat.append(self._gen_tree(1))
          total += root.subcat[-1].total
          os.chdir('../')

    root.total = total

    self.info['TestTree'] = root
    return self.info


  def _gen_tree(self, level):
    """
      Method that will parse subdirectories to find all files
      and build a TestTree with it
    """
    # Create a new node
    prefix = os.getcwd()
    cat_name = os.path.basename(prefix)
    cat = TestTree(level, prefix, cat_name)
    cat.info = self._readInfo()

    for f in os.listdir(prefix):
      if f == "__modules":
        continue
      if os.path.isdir(f):
        os.chdir(f)
        cat.subcat.append(self._gen_tree(level + 1))
        cat.total += cat.subcat[-1].total
        os.chdir('../')
      elif level > 0:
        cat.tests.append(Test(prefix, f, cat_name))

    cat.total += len(cat.tests)

    return cat


  def _readInfo(self):
    """
      Read the info file and return a dictionary that contains
      informations on this categorie's tests
    """
    info_tmp = dict(self.info)
    if os.path.exists("info"):
      f = file("info")
      lines = f.read().split('\n')
      for line in lines:
        if line is not '':
          option = line.split('=')
          if option[1] and option[0]:
            info_tmp[option[0]] = option[1]
    else:
      info = None

    return info_tmp
