###############################################################################
#                                                                             #
#    This file is part of the PyCheck project                                 #
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



import sys, os, fnmatch, glob
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
    self.max_cat = 5
    self.info = info
    root = TestTree(0, '', 'Total')
    total = 0
    
    tmp_path = os.getcwd()

    # Visit each path to find tests
    for path in self.info['test_path']:
      if path in info['blacklist']:
        continue
        os.chdir(tmp_path)
      path = os.path.expanduser(path)
      try:
        os.chdir(path)
      except:
        continue
      for f in os.listdir(os.getcwd()):
        if os.path.isdir(f) and self._is_dir_valid(f):
          try:
            os.chdir(f)
          except:
            continue
          tmp = self._gen_tree(1)
          if tmp.total:
            if len(tmp.cat) > self.max_cat:
              self.max_cat = len(tmp.cat)
            root.subcat.append(tmp)
            total += tmp.total
          os.chdir('../')

    root.total = total
    self.info['TestTree'] = root
    self.info['max_cat_len'] = self.max_cat

    return self.info


  def _gen_tree(self, level):
    """
      Method that will parse subdirectories to find all files
      and build a TestTree with it
    """
    # Get path prefix and category name
    prefix = os.getcwd()
    cat_name = os.path.basename(prefix)

    # Create a new node
    cat = TestTree(level, prefix, cat_name)
    cat.info = self._readInfo()

    # Call the prelude function
    prelude_cat(cat.info)


    # Visit files and subdir
    for f in os.listdir(prefix):
      # Parse subdir and maj test_list
      if os.path.isdir(f) and self._is_dir_valid(f):
        try:
          os.chdir(f)
        except:
          continue
        tmp = self._gen_tree(level + 1)
        if tmp.total:
          cat.subcat.append(tmp)
          cat.total += tmp.total
        os.chdir('../')
      elif self._is_file_valid(f):
        cat.tests.append(Test(prefix, f))

    cat.total += len(cat.tests)

    return cat


  def _is_dir_valid(self, d):
    """
      Check if a directory is correct according to categories options
      and blacklist
    """
    # Check blacklist
    if d in self.info['blacklist']:
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
    if f in self.info['blacklist']:
      return False

    # Check ignore list
    for pat in self.info['ignore']:
      if fnmatch.fnmatch(f, pat):
        return False

    # Check file_ext
    for pat in self.info['file_ext']:
      if fnmatch.fnmatch(f, pat):
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
          if len(option) > 1 and option[1] and option[0]:
            info_tmp[option[0]] = option[1]

    return info_tmp
