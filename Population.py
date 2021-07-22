''' Program to plot the "population non_linear equation" interations. The equation is
 x[n+1] = rho * x[n] * (1 = x[n])
 
MIT License

Copyright (c) 2021 Darwin Geiselbrecht

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import pygame, sys, time, random, math
from pygame.locals import *

pygame.init()

WINDOWWIDTH = 2100
WINDOWHEIGHT =1300

BLACK = (0,0,0)
WHITE =  (255,255,255)
YELLOW = (255,255,0)
LIGHTYELLOW = (128,128,0)
RED = (255, 0 ,0)
LIGHTRED = (128,0,0)
BLUE = (0, 0, 255)
SKYBLUE = (135,206,250)
GREEN = (0,255,0)
LIGHTGREEN = (152,251,152)
AQUAMARINE = (123,255,212)
LIGHTBROWN = (210,180,140)
LIGHTGREY = (211,211,211)
DIMGREY = (105,105,105)
VIOLET = (238,130,238)
SALMON = (250,128,114)
GOLD = (255,165,0)
BACKGROUND = LIGHTGREY
ORANGE = (255,140,0)


windowSurface = pygame.display.set_mode([WINDOWWIDTH, WINDOWHEIGHT])
pygame.display.set_caption('Population')


#--------------------------------------------------------------------------
# Routine to output a pixel
# xpixel is the pixel numbrer of the x cooridinate in pixels
# ynorm is a x between 0.0 and 1.0 giving the value of the equation to be plotted
# y_low is the lower limit of ynorm that is to be plotted
# y_high is the upper limit of y_norm that is to be plotted
# color is the color
#--------------------------------------------------------------------------

def plot(xpixel, ynorm, y_low, y_high,color):
  
  y_range = y_high - y_low
  y_rescale = 1.0 / y_range
  y_renorm = (ynorm - y_low) * y_rescale # renormalized to the range of y_high - y_low
  ypixel = int( WINDOWHEIGHT - (y_renorm*WINDOWHEIGHT)) # compute ypixel
  if (ypixel <0):
    ypixel = 0
  elif (ypixel >= WINDOWHEIGHT):
    ypixel = WINDOWHEIGHT

  
  pygame.draw.circle(windowSurface,color,(xpixel, ypixel), 0 )

  return
#--------------------------------------------------------------------------
# Routine to get the current cursor position in terms of rho and x
# returns current rho, current x
#--------------------------------------------------------------------------

def get_cursor(begin_rho,end_rho,low_x,high_x):

  xpos,ypos = pygame.mouse.get_pos()
  cur_rho = begin_rho + ((end_rho -begin_rho) ) * (xpos/WINDOWWIDTH)
  cur_x =  low_x + (high_x - low_x) * (WINDOWHEIGHT - ypos) / WINDOWHEIGHT

  return cur_rho, cur_x
#--------------------------------------------------------------------------
# Routine to zoom based on cursor position
# called with  beginning and ending rho, low and high x range to plot and
# zoom ratio.  A ratio greater than one is a zoom in, a rattio less than one
# results in a zoom out.
#--------------------------------------------------------------------------
def zoom(begin_rho,end_rho,low_x,high_x,zoom_ratio):

  cur_rho, cur_x = get_cursor(begin_rho,end_rho,low_x,high_x)


  rho_range = end_rho - begin_rho  # compute range of rho and compute end points
  begin_rho = cur_rho - (rho_range/zoom_ratio)/2.
  end_rho = cur_rho + (rho_range/zoom_ratio)/2.

  if begin_rho < 0.:    # ensure rho stays in range
    begin_rho = 0.
  if end_rho > 4.:
    end_rho = 4. 

  x_range = high_x - low_x    # compute range of x  and compute end points
  low_x = cur_x - (x_range/zoom_ratio)/2.
  high_x = cur_x + (x_range/zoom_ratio)/2.

  if low_x < 0:         # ensure x stays in range
    low_x = 0.
  if high_x > 1.:
    high_x = 1.
    
  print(begin_rho,end_rho,low_x,high_x)

  return begin_rho,end_rho,low_x,high_x


#--------------------------------------------------------------------------
# Routine to do the calculations and output the plot
# called with beginning x, beginning and ending rho, low and high x range to plot
#--------------------------------------------------------------------------

def plot_population(beg_value,beg_rho,end_rho,low_value,high_value):

  windowSurface.fill(BLACK)       # clear plot window
  pygame.display.update()

  rho_inc = (end_rho - begin_rho) / WINDOWWIDTH # compute number of rho xs to plot

  num_plots = (end_rho - begin_rho) / rho_inc
  x = 0     # start at left of window
  x_delta = WINDOWWIDTH/num_plots


  rho = begin_rho

  while rho <= end_rho :

    value = beg_value
    plot_count = 0      # number of points plotted for this rho
    for i in range(1,100000):
      value = value * rho * (1-value)
      if (value > low_value and value < high_value ):
        plot (int(x) , value,low_value,high_value,WHITE)
        plot_count = plot_count + 1

      if plot_count > (.75 * WINDOWHEIGHT):       # auto density to avoid white out 
        break
      elif (i > 10000) and (plot_count == 0):      # bail on completely dark rho value
        break

    pygame.display.update()
    pygame.event.pump()
    x = x + x_delta
    rho = rho + rho_inc

  return

#--------------------------------------------------------------------------
# Start of Mainline code
#--------------------------------------------------------------------------

# Set up the default variables

begin_value = .5
zoom_ratio = 4.
begin_rho = 3.5
end_rho = 4.0
low_x = 0.
high_x = 1.

plot_population(begin_value,begin_rho,end_rho,low_x,high_x)

while True:

  for event in pygame.event.get():
    if event.type == QUIT:
        pygame.quit()
        sys.exit()

    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # left button is number 1, zoom in
        begin_rho,end_rho,low_x,high_x = zoom(begin_rho,end_rho,low_x,high_x,zoom_ratio)
        plot_population(begin_value,begin_rho,end_rho,low_x,high_x)        

    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:  # right button is number 3, zoom out
        begin_rho,end_rho,low_x,high_x = zoom(begin_rho,end_rho,low_x,high_x,1./zoom_ratio)
        plot_population(begin_value,begin_rho,end_rho,low_x,high_x)  
            
  time.sleep(1.)

#pygame.quit()
#sys.exit
