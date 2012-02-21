from display import *
from subprocess import *
from threading import *
from tempfile import NamedTemporaryFile
import sys, os


cat = {}
fails = []


class Test():
  """
    Class that represents a test which failed
  """
  def __init__(self, c, name, process, expected, desc, output = '', error = '', diff = ''):
    self.cat = c
    self.name = name
    self.process = process
    self.expec = expected
    self.desc = desc
    self.output = output
    self.error = error
    self.diff = diff

  def __print__(self):
    """
      Print the details about this test
    """
    codes = '(expected : \033[32m' + str(self.expec) + \
      '\033[37m returned : \033[31m' +                 \
      str(self.process.returncode) + '\033[37m)'
    names = '\033[34m' + self.cat + ' -> \033[33m' + self.name + '\033[37m' 
    decal = lar - len(codes) - len(names) + 7 * len('\033[37m')
    print names, ' ' * decal, codes
    if self.desc:
      print '   \033[36mdescription\033[37m = ' + self.desc
    stdout = [m for m in self.process.stdout.read().split('\n') if m]
    if len(stdout):
      print '   \033[32mstdout\033[37m : ' + stdout[0]
    stderr = self.process.stderr.read()
    if len(stderr) or len(self.error):
      print '   \033[31mstderr\033[37m : '+ stderr + '\033[32m-----\033[37m\n' + self.error
    if self.output:
      print '\033[34m       Pretty-print :\033[37m'
      print self.output
    if self.diff:
      print '\033[34m       Diff :\033[37m'
      print self.diff


def get_desc(f):
  """
    Get the first comment of the file (do not support recursive comments)
  """
  right = [f for f in file(f).read().split('/*') if f][1:]
  if not right:
    return None
  return right[0].split('*/')[0]


def try_pprint(process, binary):
  """
    Test the pretty-print function of the tiger compiler
  """
  output = process.stdout.read()
  
  # Create a tmp file with the stdout of the first process
  tmpFile = NamedTemporaryFile()
  tmpFile.write(output)
  tmpFile.flush()

  # Lauch a secon process on it
  p = Popen([binary, '--ast-display', tmpFile.name], stderr=PIPE, stdout=PIPE, shell=False)
  p.wait()

  to_compare = p.stdout.read()

  tmpFile1 = NamedTemporaryFile()
  tmpFile1.write(to_compare)
  tmpFile1.flush()

  diff = Popen(['diff', tmpFile1.name, tmpFile.name], stdout=PIPE, shell=False)
  diff.wait()
  diff_ = diff.stdout.read()

  tmpFile.close()
  tmpFile1.close()
  return output == to_compare, '\033[32m-----\033[37m\n'.join([output, to_compare]), p.stderr.read(), diff_


def launch_test(f, info, level, c):
  """
    Launch the tc binary on file f and checking returncode with info
  """
  if info:
    binary = '../' * (level) + '/tc'
    if 'flags' in info:
      flags = [x for x in info['flags'].split(' ') if x]
      p = Popen([binary] + flags + [f], stderr=PIPE, stdout=PIPE, shell=False)
    else:
      p = Popen([binary, f], stderr=PIPE, stdout=PIPE, shell=False)
    p.wait()
    # launch the pretty_print test
    result, output, error, diff = try_pprint(p, binary)

    if str(p.returncode) is info['return'] and result:
      return success(f, info)
    else:
      fails.append(Test(c, f, p, info['return'], get_desc(f), output, error, diff))
      return fail(f, info, False, p)
  else:
    print "No info file is present in the directory"
    return 0


def launch_test_pp(f, info, level, c):
  """
    Launch the tc binary on file f and checking returncode with info
  """
  if info:
    binary = '../' * (level) + '/tc'
    if 'flags' in info:
      flags = [x for x in info['flags'].split(' ') if x]
      p = Popen([binary] + flags + [f], stderr=PIPE, stdout=PIPE, shell=False)
    else:
      p = Popen([binary, f], stderr=PIPE, stdout=PIPE, shell=False)
    p.wait()
    # launch the pretty_print test

    if str(p.returncode) is info['return']:
      return success(f, info)
    else:
      fails.append(Test(c, f, p, info['return'], get_desc(f)))
      return fail(f, info, False, p)
  else:
    print "No info file is present in the directory"


def readInfo():
  """
    Read the info file and return a dictionnary that contains
    informations on this categorie's tests
  """
  info = {}
  if os.path.exists("info"):
    f = file("info")
    lines = f.read().split('\n')
    for line in lines:
      if line is not '':
        option = line.split('=')
        if option[1] and option[0]:
          info[option[0]] = option[1]
  else:
    info = None

  return info


def parse_cat(level):
  """
    List subdirectories' content en launch test on each file
  """
  c = os.path.basename(os.getcwd())
  printHeader(c, level)
  info = readInfo()

  if 'all' in cat and c not in cat:
    cat[c] = [0, 0]

  files = []
  parent = os.getcwd()

  for f in os.listdir(parent):
    if os.path.isdir(f):
      os.chdir(f)
      parse_cat(level + 1)
      # add results of the subcategories to the categorie
      cat[os.path.basename(parent)][0] += cat[os.path.basename(os.getcwd())][0]
      cat[os.path.basename(parent)][1] += cat[os.path.basename(os.getcwd())][1]
      os.chdir('../')
    elif level > 0:
      files.append(f)

  if c in cat:
    for f in files:
      if f != 'info':
        if c == 'good':
          cat[os.path.basename(os.getcwd())][launch_test(f, info, level, c)] += 1
        else:
          cat[os.path.basename(os.getcwd())][launch_test_pp(f, info, level, c)] += 1
