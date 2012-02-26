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


import sys, os, re
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
    
    # Compile regexp for file extension
    file_ext = info['file_ext']
    for line, pattern in enumerate(file_ext):
      info['file_ext'][line] = re.compile(pattern)

    # Compile regexp for blacklist
    blacklist = info['black_list']
    for line, pattern in enumerate(blacklist):
      info['black_list'][line] = re.compile(pattern)

    tmp_path = os.getcwd()
    # Visit each path to find tests
    for path in self.info['test_path']:
      os.chdir(tmp_path)
      path = os.path.expanduser(path)
      os.chdir(path)
      for f in os.listdir(path):
        if os.path.isdir(f) and self._is_dir_valid(f):
          os.chdir(f)
          tmp = self._gen_tree(1)
          if tmp.total:
            root.subcat.append(tmp)
            total += tmp.total
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

    # Visit files and subdir
    for f in os.listdir(prefix):
      # Parse subdir and maj test_list
      if os.path.isdir(f) and self._is_dir_valid(f):
        os.chdir(f)
        tmp = self._gen_tree(level + 1)
        if tmp.total:
          cat.subcat.append(tmp)
          cat.total += tmp.total
        os.chdir('../')
      elif self._is_file_valid(f):
        cat.tests.append(Test(prefix, f, cat_name))

    cat.total += len(cat.tests)

    return cat

  def _is_dir_valid(self, d):
    """
      Check if a directory is correct according to categories options
      and blacklist
    """
    # Check blacklist
    for pat in self.info['black_list']:
      if pat.match(d):
        return False

    if 'all' in self.info['categories']:
      return True
    if d in self.info['categories']:
      return True

    return False


  def _is_file_valid(self, f):
    """
      Check if a file is valid according to blacklist and file_ext
    """
    # Check blacklist
    for pat in self.info['black_list']:
      if pat.match(f):
        return False

    # Check file_ext
    for pat in self.info['file_ext']:
      if pat.match(f):
        return True

    return False


  def _readInfo(self):
    """
      Read the info file and return a dictionary that contains
      informations on this categorie's tests
    """
    info_tmp = dict(self.info)
    if os.path.exists("info") and not os.path.isdir("info"):
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
