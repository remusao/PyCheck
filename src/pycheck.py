#! /usr/bin/python2
# -*- coding: iso-8859-15 -*-

from parse import *
import argparse

try:
  from graph import *
  pygame_exists = True
except ImportError:
  pygame_exists = False


"""
This program aims at testing the TC projet which is a tiger compiler written
with the C++ langage, bison and flex.
"""


def parseArg():
  """
    Parse arguments given to the test_suit program
  """
  parser = argparse.ArgumentParser(description='Test suit that aims to  \
    test the TC project which is a tiger compiler writter in C++ and  \
    using flex / bison to generate the lexer / parser.')
  parser.add_argument('--version', action='version', version='%(prog)s for TC0')
  parser.add_argument('-c', nargs='+', default=['all'], metavar='categorie' ,help='Launch the tests present in \
      the given (sub)categorie(s).')

  return parser.parse_args()



def main():
  """
    Parse arguments, launch the test_suit and display the results
  """

  args = parseArg()

  for c in args.c:
    cat[c] = [0, 0]

  parse_cat(0)
  result(cat)

  connection = db_init()
  cursor = connection.cursor()
  db_create_if_need(cursor)
  db_insert(cursor, cat['all'][0], cat['all'][1])


  if pygame_exists:
    t = raw_input('\n\nDo you want to print the graph ? (Y/n) ')
    if t == 'Y' or t == 'y':
      graph(cat, cursor)

  connection.commit()
  connection.close()

  if fails:
    t = raw_input('Do you want to sum-up fails ? (Y/n) ')
    print
    if t == 'Y' or t == 'y':
      for i in fails:
        i.__print__()
    print

if __name__ == "__main__":
  main()
