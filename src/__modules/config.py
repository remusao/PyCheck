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

################################################################################
#
#   This is the configure file of your PyCheck test_suit.
#   You can specify here options that will interract with the test_suit.
#   There exists some builtins options that are listed bellow, but you
# can create your own. They will be present in the info dict with the form
#     info['option'] = 'value'
#
#   Be warned that this options will apply on all the tests. If you want to apply
# an option on a single category, you can override this option in the info file
# present in your category's directory.
#
#   You can override this options with command line options of the same names or,
# if they are not present, with an option of the form :
#     --other option=value
################################################################################



class Config():

  def __call__(self, info):

    #self.info = self.info

    ############################## __ TEST_PATH __  ############################
    # This option specifies where the test_suit will look for your tests. You can
    # specify as many path as you like, whithin a list
    # Type = [string]
    # Default = ./

    info['test_path'] = ['./']


    ############################### __ FILE_EXT __  ############################
    # This option specifies what extension the test_files must have. Give a regexp
    # type = [string]
    # Default = ['*']

    info['file_ext'] = ['.*']


    ############################### __ BLACKLIST __  ###########################
    # This option specifies a black list if you want to avoid some files or
    #  directories
    # type = [string]
    # Default = []

    info['black_list'] = ['__.*', '*.swp', 'info']


    ############################ __ MULTITHREADING __ ##########################
    # This option specifies if you want to multithread the execution of your tests
    # Type = bool
    # Default = False

    info['multithreading'] = False


    ############################ __ MEMCHECK __  ###############################
    # Specifies if you want to check leaks on your tests. Be warned that this is
    # time consuming and you should preferably add this option in an info file to
    # check leaks only on a single category.
    # Type = bool
    # Default = False

    info['memcheck'] = False


    ############################ __ TIMEOUT __  #################################
    # Specifies if you want to check a timeout on every tests
    # Type = int (in ms)
    # Default = 0

    info['timeout'] = 0


    ############################## __ VERBOSE __ ###############################
    # This option specifies if you want a verbose output for you test_suit.
    #   - If True, the result of each test will be printed
    #   - If False, only the summary will be printed
    # Type = bool
    # Default = True

    info['verbose'] = True


    ############################ __ PRETTYPRINT __ #############################
    # This option specifies if you want the testTree to be pretty-printed
    # Type = bool
    # Default = False

    info['prettyprint'] = False


    ############################### __ OUTPUT __ ###############################
    # This option specifies if you want some output (graph, db, etc..)
    # Type = [string]
    # Default = ['graph', 'db']

    info['output'] = ['db']


    ############################################################################
    ################################ __ CUSTOM __ ##############################
    ############################################################################
    # You can now specify as many custom options as you like with the form :
    #   info['option'] = value
    # You will be able to use it on your tests and access it with the info arg
    # of the __call__ method of the Test() object.

    # Exemple
    # info['answer'] = 42



    return info
