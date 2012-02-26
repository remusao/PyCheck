#! /usr/bin/python2
# -*- coding: iso-8859-15 -*-
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

import sys

sys.path.append('__modules')
from Customize_me import *
from config import Config
from get_tests import Build
from parse_arg import Parse_arg
from run_tests import Run
from output import Output


class Task():
  """
    Design pattern command. Will manage every task
    of the test_suit. You can add as many tasks as
    you want. You can then run them by calling the
    Task object
  """

  def __init__(self):
    """
      Init an empty task list
    """
    self.tasks = []


  def add(self, task):
    """
      Add a task in the task list
    """
    self.tasks.append(task)


  def __call__(self):
    """
      Run the tasks one by one
    """
    result = {}
  #  try:
    for task in self.tasks:
      result = task(result)
  #  except Exception as e:
  #    print e
  #  finally:
    return result



def main():

  # Prolog
  logo_print()
  prelude()

  # Create the task manager
  task = Task()

  # Add tasks
  task.add(Config())
  task.add(Parse_arg())
  task.add(Build())
  task.add(Run())
  task.add(Output())

  # Launch tasks
  result = task()

  # Call the 
  epilog()


if __name__ == '__main__':
  main()
