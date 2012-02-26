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

    if out_list:
      # sumup test that failed and print details about them
      if 'sumup' in out_list:
        self._sumup()
      # Log results in db and print graph
      if 'graph' in out_list and 'db' in out_list:
        self._db_graph()
    if 'prettyprint' in self.info:
      if self.info['prettyprint']:
        print
        self.info['TestTree'].pretty_print()

    return info


  def _db_graph (self):
    """
      Log results in the db and display the graph
    """
    connection = db_init()
    cursor = connection.cursor()

    db_create_if_need(cursor)
    print self.info['TestTree'].success
    print self.info['TestTree'].fail
    db_insert(cursor, self.info['TestTree'].success,
                      self.info['TestTree'].fail)

    cat = {}
    for sub in self.info['TestTree'].subcat:
      cat[sub.cat] = (sub.success, sub.fail)
    graph(cat, cursor)

    connection.commit()
    connection.close()


  def _sumup(self):
    """
      Display the tests that failed with useful informations
    """
    return
