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


from Customize_me import Test
from test_tree import TestTree
from display import printHeader
from db import *
from graph import *


class Output():
  """
    This task manage every form of output (graph, db, etc.).
  """

  def __call__(self, info):
    """
      Will check if options are present in the info['output'] and
      run actions if it's the case
    """
    self.info = info
    out_list = info['output']

    if self.info['prettyprint']:
      out_list.append('prettyprint')

    if out_list:
      for module in out_list:
        self._launch_output(module)
    print

    return info


  def _launch_output(self, name):
    """
      Given a module name (or whatever), will launch the good output
    """
    if name is 'sumup':
      print
      printHeader('# Fails Summary #', 1)
      print
      self._sumup()
    elif name is 'graph':
      print
      printHeader('# Graph #', 1)
      print
      self._db_graph()
    elif name is 'prettyprint':
      print
      printHeader('# Pretty Printing #', 1)
      print
      confirm = raw_input('Do you want to pretty_print the TestTree ? (y/n) ')
      if confirm == 'y' or confirm == 'Y':
        self.info['TestTree'].pretty_print()


  def _db_graph (self):
    """
      Log results in the db and display the graph
    """
    tree = self.info['TestTree']
    connection = db_init()
    cursor = connection.cursor()

    db_create_if_need(cursor)
    db_insert(cursor, tree.success, tree.fail)

    confirm = raw_input('Do you want to display the graph ? (y/n) ')
    if confirm == 'y' or confirm == 'Y':
      cat = {}
      for sub in tree.subcat:
        cat[sub.cat] = (sub.success, sub.fail)
      cat['all'] = (tree.success, tree.fail)
      graph(cat, cursor)

    connection.commit()
    connection.close()


  def _sumup(self):
    """
      Display the tests that failed with useful informations
    """
    confirm = raw_input('Do you want to display a sum-up ? (y/n) ')
    if confirm != 'y' and confirm != 'Y':
      return


    for sub in self.info['TestTree'].subcat:
      self._print_rec_sumup(sub)


  def _print_rec_sumup(self, tree):
    """
      Parse the TestTree to display a sumup about tests that failed
    """
    # sumup_print()
    for t in tree.tests:
      if not t.result:
        print '\033[32m', tree.cat, '\033[37m', '-->', '\033[33m', t.f, '\033[37m'
        t.sumup_print()
        print
    for sub in tree.subcat:
      self._print_rec_sumup(sub)
