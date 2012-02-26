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


from test_tree import TestTree


lar = 80
#lar = os.environ['COLUMNS']  #width of the result form


def printSuccess(f):
  """
    Print the right output in case of success
  """
  print f + ' ' * (lar - len(f) - 2) + '\033[32m' + 'OK' + '\033[37m'


def printFail(f, error):
  """
    Print the right output in case of fail (wrong returncode or timeout)
  """
  col = '\033[37m' * (error[0] + 2)
  m = error[1] + '\033[31m' + '   KO' + '\033[37m'
  print f + ' ' * (lar - len(m) - len(f) + len(col)) +  m


def printHeader(c, level):
  """
    Write the right header according to the category and its level
  """
  if level is 1:
    mult = (lar - len(c)) / 2
    print '\033[34m' + '_' * lar
    print '\n\033[35m' + ' ' * mult + c, '\033[34m'
    print '_' * lar + '\033[37m\n'
  if level > 1:
    print '\n\033[36m--> Subcategorie :\033[35m', c, '\033[37m\n'


def printBar(cat, result, catMaxi, maxiFail, maxiSucc):
  """
    Print a progress bar in a htop-like style
  """
  if result[0] + result[1]:
    decal = catMaxi - len(cat) + 2  # number of spaces between catName and bar start
    size = lar - catMaxi - 15       # size of the bar
    r = int((float(result[0]) / float(result[0] + result[1])) * size) # width of the section with '..|||..' in the bar
    succ = '\033[32m' + str(result[0]) + '\033[37m'                   # Number of success
    fail = '\033[36m' + str(result[1] + result[0]) + '\033[37m'       # Number of fails
    decEnd = len(str(maxiFail)) + len(str(maxiSucc)) + 4 * len('\033[37m') - len(succ) - len(fail) + 1 # number of spaces before recap
    pourcent = str(int(float(result[0]) / float(result[1] + result[0]) * 100.0)) # pourcentage of success

    bar = ['\033[34m' + cat + '\033[37m']                     # cat name
    bar.append(' ' * decal)                                   # decal before the bar
    bar.append(' [')                                          # begining of the progress bar
    bar.append('|' * r + ' ' * (size - r))                    # print enough pipes '..|||||..'
    bar.append(' ' * (decEnd) + succ + '/' + fail)            # print spaces and recap
    bar.append(']')                                           # close the progress bar
    bar.append(' ' * (4 - len(pourcent)) + pourcent + '%')    # print the percentage of success

    # Insert color in the progres bar
    bar[3] = '\033[31m' + bar[3][:size / 3] + '\033[33m' + \
                  bar[3][size/3:2 * size/3] + '\033[32m' + \
                  bar[3][2*size/3:size] + '\033[37m'

    # Print the result bar
    print ''.join(bar)


def get_max(tree):
  """
    Parse the cat list and get :
      0) The len of the longest category's name
      1) The len of the maximum number of success
      2) The len of the maximum number of fails
  """
  maxi = [len(tree.cat), tree.success, tree.fail]

  for sub in tree.subcat:
    max_name, max_succ, max_fail = get_max(sub)
    maxi[0] = max(max_name, maxi[0])
    maxi[1] = max(max_succ, maxi[1])
    maxi[2] = max(max_fail, maxi[2])

  return maxi


def result_rec(tree, maxi):
  """
    Parse the tree and print a htop bar for each main category
  """
  printBar(tree.cat, (tree.success, tree.fail), maxi[0], maxi[1], maxi[2])


def printResult(tree):
  """
    Print the results in a beautiful form
  """
  print
  printHeader('# Summary #', 1)
  print
  maxi, maxiSucc, maxiFail = get_max(tree)

  for sub in tree.subcat:
    result_rec(sub, (maxi, maxiFail, maxiSucc))

  # Print the total
  print
  printBar('Total', (tree.success, tree.fail), maxi, maxiFail, maxiSucc)
