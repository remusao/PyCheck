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


from pygame.locals import *
import pygame, math, sys
from db import *

# Some constants about rendering

webradius = 300
web_anim_speed = 7
progress_max = webradius / web_anim_speed

# colors
textcolor = (100,100,255,0)
linecolor = (255,255,0,0)
shapecolor = (255,0,0,0)
polygoncolor = (25, 125, 75, 0)
mark_color = (255, 255, 0, 0)
total_curve_color = (0, 0, 255, 0)
fail_curve_color = (255, 0, 0, 0)
success_curve_color = (0, 255, 0, 0)

# WEB GRAPHIC

def get_regular_polygon(center, sides, radius):
  """
    Return a list of points that represent a regular polygon defined by :
    a number of 'sides' sides, centered on 'center'
  """
  angle = 2 * math.pi / sides
  pointlist = []
  for i in range(0, sides):
    pointlist += [(center[0] + radius * math.cos (i * angle - math.pi / 2),
                   center[1] + radius * math.sin (i * angle - math.pi / 2))]
  return pointlist

def get_web(center, pointlist, cat, progress):
  web = []
  i = 0
  cat2 = cat
  newcenter = [0,0]
  for c in cat:
    if (c != 'tests' and c != 'all'):
      newcenter[0] = (pointlist[i][0] - center[0]) * 0.05 + center[0]
      newcenter[1] = (pointlist[i][1] - center[1]) * 0.05 + center[1]
      if (cat[c][1] + cat[c][0] != 0):
        Xp = (float(pointlist[i][0] - float(newcenter[0])))  * \
            (float(cat[c][0]) * 0.995 / (float(cat[c][0] + cat[c][1]))) +\
            float(newcenter[0])
        Yp = (float(pointlist[i][1] - float(newcenter[1]))) * \
            (float(cat[c][0]) * 0.995 / (float(cat[c][0] + cat[c][1]))) +\
            float(newcenter[1])
        web += [(Xp, Yp)]
      else:
        web += [(newcenter[0], newcenter[1])]
      i+= 1
  return web

def print_text(text, pos):
  font = pygame.font.SysFont("Modern Computer",25)
  ren = font.render(text,1,textcolor)
  pygame.display.get_surface().blit(ren,\
                                    (pos[0] - ren.get_width() / 2,  pos[1]))


def display_cat(cat, pointlist, center):
  i = 0
  for c in cat:
    if (c != 'test' and c != 'all'):
      print_text(c, ((pointlist[i][0] - center[0]) * 1.1 + center[0],\
                       (pointlist[i][1] - center[1]) * 1.1 + center[1]))
      i+=1

def draw_web_graph(cat, pointlist, web, center):
    pygame.draw.aalines(pygame.display.get_surface(),           \
                          (shapecolor), True,                   \
                          pointlist)
    pygame.draw.polygon(pygame.display.get_surface(),
                        (polygoncolor),
                        web)
    for i in range(0, len(pointlist)):
      pygame.draw.aaline(pygame.display.get_surface(),
                         (linecolor),
                         center, pointlist[i])
    display_cat(cat, pointlist, (center))


# END WEB GRAPHIC




# DATABASE PRINTER



def draw_mark(scrsize, origin):
  pygame.draw.aaline(pygame.display.get_surface(), mark_color,          \
                       origin,                                          \
                       (8.0 * float(scrsize[0]) / 10.0 + origin[0],
                        origin[1]))
  pygame.draw.aaline(pygame.display.get_surface(), mark_color,          \
                       origin,                                          \
                      (origin[0],
                       origin[1] - 9.0 * float(scrsize[1]) / 10.0))

# origin is the position of the origin of the mark
# marksize is the length of the mark (x, y)
# value_list is the list of values that will be drawn
# value_max is the maximum value of this list
# color is the color of the curve to draw
def draw_curve(origin, marksize, value_list, value_max, color, progress):
  pointlist = []
  for i in range(0,
                 (len(value_list) < progress and len(value_list) or progress)):
    pointlist += [(origin[0] + float(i)/ float(len(value_list)) * marksize[0],\
         origin[1] - float(value_list[i][0]) / float(value_max) * marksize[1])]
  pygame.draw.aalines(pygame.display.get_surface(), color, \
                        False, pointlist)
  if (len(value_list) < progress):
    print_text(str(value_list[len(value_list) - 1][0]),
               (pointlist[len(pointlist) - 1][0] + 25,
                pointlist[len(pointlist) - 1][1] - 8))


def draw_legend(origin, marksize):
  ltotal = [(origin[0] + 0.1 * marksize[0],
             origin[1] - 1.2 * marksize[1])]
  ltotal += [(origin[0] + 0.2 * marksize[0],
              origin[1] - 1.2 * marksize[1])]
  lsuccess = [(origin[0] + 0.4 * marksize[0],
               origin[1] - 1.2 * marksize[1])]
  lsuccess += [(origin[0] + 0.5 * marksize[0],
                origin[1] - 1.2 * marksize[1])]
  lfail = [(origin[0] + 0.75 * marksize[0],
               origin[1] - 1.2 * marksize[1])]
  lfail += [(origin[0] + 0.85 * marksize[0],
                origin[1] - 1.2 * marksize[1])]
  pygame.draw.aaline(pygame.display.get_surface(), total_curve_color,
                     ltotal[0], ltotal[1])
  pygame.draw.aaline(pygame.display.get_surface(), success_curve_color,
                     lsuccess[0], lsuccess[1])
  pygame.draw.aaline(pygame.display.get_surface(), fail_curve_color,
                     lfail[0], lfail[1])
  print_text("Legend:", (origin[0], origin[1] - 1.2 * marksize[1] - 8))
  print_text("Total", (ltotal[1][0] + 35, ltotal[1][1] - 8))
  print_text("Success", (lsuccess[1][0] + 45, lsuccess[1][1] - 8))
  print_text("Fail", (lfail[1][0] + 25, lfail[1][1] - 8))

# END DATABASE PRINTER


#cat is the dictionnary caintaining all the results
#cur is the cursor get when openning a new connection
def graph(cat, cursor):
  """ Print the results in a graph """

# initialize the graph module
  pygame.init ()
  size_web = wi, he = 750, 750
  size_graph = wi2, he2 = wi, 200
  size = wit, het = wi, he + he2
  screen = pygame.display.set_mode(size)
  pygame.display.set_caption("pygame window : TC test-suite results")

  # compute the angles of the shapes
  pointlist = get_regular_polygon((wi/2, he/2 - 40), len(cat) - 1, webradius)

  # compute the datas for the second graph
  origin = (float(size_graph[0]) / 10.0, 9.0*float(size_graph[1])/ 10.0 + \
      size_web[1])
  marksize = (8.0*float(size_graph[0])/ 10.0, 9.0*float(size_graph[1])/ 10.0)
  top = db_get_max(cursor) # get the top value of the graph
  total_list = db_get_total(cursor) # get the list of total values
  success_list = db_get_success(cursor) # get the list of success
  fail_list = db_get_fail(cursor) # get the list of fails
  max_success = db_get_max_success(cursor)

  web_anim_speed = 300.0 / len(total_list)
  progress_max = webradius / web_anim_speed

  db_print(cursor)

  stop = True
  progress = 1
# main loop
  while stop:
    progress += 1
    # event handling
    for event in pygame.event.get():
      if (event.type) is pygame.QUIT: stop = False
    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[pygame.K_ESCAPE]: stop = False
    if pressed_keys[pygame.K_SPACE]: progress += 10
    # web graph drawing
    web = get_web((wi/2, he/2 - 40), progress < progress_max and
                  get_regular_polygon((wi/2, he/2 - 40), len(cat) - 1,
                                      progress * web_anim_speed) or
                  pointlist
                  , cat, progress + 65)
    draw_web_graph(cat, pointlist, web, (wi/2, he/2 - 40))

    # db display
    draw_mark(size_graph, origin)
    draw_legend(origin, marksize)
    draw_curve(origin, marksize, total_list, top, total_curve_color, progress)
    draw_curve(origin, marksize, success_list, top,
               success_curve_color, progress)
    draw_curve(origin, marksize, fail_list, top, fail_curve_color, progress)

    pygame.display.flip()
  pygame.display.quit()
