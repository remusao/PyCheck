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

import threading
import Queue


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
    t = self.info['TestTree']
    mcat = self.info['max_cat_len']
    tot_success, tot_fail = 0, 0

    if self.info['verbose']:
      for sub in t.subcat:
        printHeader(sub.cat, 1)
        if self.info['multithreading']:
          tmp_success, tmp_fail = self._run_multithread(sub, self._print_verbose)
        else: 
          tmp_success, tmp_fail = self._run_tests(sub, self._print_verbose)
        tot_success += tmp_success
        tot_fail += tmp_fail
      t.success, t.fail = tot_success, tot_fail
      printResult(t)
    else:
      for sub in t.subcat:
        printHeader(sub.cat, 1)
        if self.info['multithreading']:
          tmp_success, tmp_fail = self._run_multithread(sub, self._print_no_verbose)
        else:
          tmp_success, tmp_fail = self._run_tests(sub, self._print_no_verbose)
        tot_success += tmp_success
        tot_fail += tmp_fail
        printBar(sub.cat, (sub.success, sub.fail), mcat, sub.fail, sub.success)
      t.success, t.fail = tot_success, tot_fail
      print
      printHeader('# Summary #', 1)
      printBar(t.cat, (t.success, t.fail), mcat, t.fail, t.success)
      print

    return self.info


  def _run_multithread(self, tree, print_res):
    """
      Exec the tests recurcively on each category
      -> Multithreading
    """
    return self._run_tests(tree, print_res)


  def _run_tests(self, tree, print_res):
    """
      Exec the tests recurcively on each category
      -> No multithreading
    """
    if self.info['verbose'] and tree.level > 1:
      printHeader(tree.cat, tree.level)
    success, fail = 0, 0

    for test in tree.tests:
      res = test(tree.info)
      if res:
        success += 1
        print_res(test.f, '', True)
      else:
        fail += 1
        print_res(test.f, test.error_get(), False)

    for sub in tree.subcat:
      tmp_succ, tmp_fail = self._run_tests(sub, print_res)
      success += tmp_succ
      fail += tmp_fail

    tree.success = success
    tree.fail = fail

    return success, fail


  def _print_verbose(self, f, mess, succ):
    """
      Print result (fail and success) when option verbose is present
    """
    if succ:
      printSuccess(f)
    else:
      printFail(f, mess)



  def _print_no_verbose(self, *nop):
    """
      If option verbose is false, call the void method
    """
    return
