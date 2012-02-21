"""
  Deals with displaying informations in the term
"""

lar = 80
#lar = os.environ['COLUMNS']  #width of the result form


def success(f, info):
  """
    Print the right output in case of success
  """
  print f + ' ' * (lar - len(f) - 2) + '\033[32m' + 'OK' + '\033[37m'
  return 0


def fail(f, info, timeout, process):
  """
    Print the right output in case of fail (wrong returncode or timeout)
  """
  if timeout:
    process.terminate()
    print 'timeout'
  else:
    col = '\033[32m' * 6
    m = '(expected : ' + '\033[32m' + info['return'] + '\033[37m' +            \
      ', returned : ' + '\033[33m' +  str(process.returncode) + '\033[37m' +   \
      ')   ' + '\033[31m' + 'KO' + '\033[37m'
    print f + ' ' * (lar - len(m) - len(f) + len(col)) +  m
    return 1


def printHeader(c, level):
  """
    Write the right header according to the categorie and its level
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


def get_max(cat):
  """
    Parse the cat list and get :
      - The maximum categorie name size
      - The maximum sucess result size
      - The maximum fail result size
  """
  maxi = 0
  maxiSucc = 0
  maxiFail = 0
  for c in cat:
    if cat[c][0] > maxiSucc:
      maxiSucc = cat[c][0]
    if cat[c][1] > maxiFail:
      maxiFail = cat[c][1]
    if len(c) > maxi:
      maxi = len(c)

  return maxi, maxiSucc, maxiFail


def result(cat):
  """
    Print the results in a beautiful form
  """
  print '\n'
  printHeader('# Summary #', 1)

  # Get the size of the longest category
  maxi, maxiSucc, maxiFail = get_max(cat)

  # Save total and remove it from the cat dic
  total = cat['src']
  cat['all'][0] = total[0]
  cat['all'][1] = total[1]
  del cat['src']

  # Print result of each cat
  for c in cat:
    if c != 'all':
      printBar(c, cat[c], maxi, maxiFail, maxiSucc)

  # Print the total
  print '\n'
  printBar('Total', total, maxi, maxiFail, maxiSucc)


