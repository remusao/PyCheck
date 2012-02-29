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


import sqlite3 as lite
import time

mark_color = (255, 255, 0, 0)
total_curve_color = (0, 0, 255, 0)
fail_curve_color = (255, 0, 0, 0)
success_curve_color = (0, 255, 0, 0)


# DATABASE MANAGEMENT

def db_init():
  return lite.connect('history.db')

def db_create_if_need(cursor):
  try:
    cursor.execute("SELECT MAX(Id) FROM History")
  except:
    cursor.execute("DROP TABLE IF EXISTS History")
    cursor.execute(                                                       \
      "CREATE TABLE History(Id INT, Date TEXT, Success INT, Fail INT, Total INT)")
    cursor.execute("INSERT INTO History(Id, Date, Success, Fail, Total) VALUES(?, ?, ?, ?, ?)", \
                     (0,"Creation: " + time.strftime("%A, %B %d, %Y"), 0, 0, 0))

def db_insert(cursor, success, fail):
  cursor.execute("SELECT MAX(Id) FROM History")
  maxid = cursor.fetchall()
  cursor.execute("INSERT INTO History(Id, Date, Success, Fail, Total) VALUES(?, ?, ?, ?, ?)", \
                   (maxid[0][0] + 1, time.strftime("%A, %B %d, %Y"), success, fail, success + fail))

def db_get_max(cursor):
  cursor.execute("SELECT MAX(Total) FROM History")
  return cursor.fetchall()[0][0]

def db_get_max_success(cursor):
  cursor.execute("SELECT MAX(Success) FROM History")
  return cursor.fetchall()[0][0]

def db_get_length(cursor):
  cursor.execute("SELECT MAX(Id) FROM History")
  return cursor.fetchall()[0][0] + 1

def db_get_total(cursor):
  cursor.execute("SELECT Total FROM History")
  return cursor.fetchall()

def db_get_success(cursor):
  cursor.execute("SELECT Success FROM History")
  return cursor.fetchall()

def db_get_fail(cursor):
  cursor.execute("SELECT Fail FROM History")
  return cursor.fetchall()

def db_print(cursor):
  """
    Print the best, worst and average tests present in the db
  """
  cursor.execute("SELECT * FROM History")
  rows = cursor.fetchall()
  avg = [0] * 2
  maxi = [0] * 3
  mini = [0] * 3
  for row in rows:
    avg[0] += row[-1]
    avg[1] += row[-2]
    if maxi[2] < row[-1]:
      maxi[0] = row[-3]
      maxi[1] = row[-2]
      maxi[2] = row[-1]
    if mini[1] < row[-2]:
      mini[0] = row[-3]
      mini[1] = row[-2]
      mini[2] = row[-1]

  avg[0] /= len(rows)
  avg[1] /= len(rows)

  print 'Best :', maxi
  print 'Worst :', mini
  print 'Average :', '  success ->', avg[0], '  fail ->', avg[1]

# END DATABASE MANAGEMENT

