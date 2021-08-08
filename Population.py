''' Program to plot the "population non_linear equation" interations. The equation is
 x[n+1] = rho * x[n] * (1 - x[n])
 
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

''' Change history
7/22/2021 add color to plots
8/7/2021 add plot of locus of the interations
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

#------------------------------------------------------------------
# Define the widget classes
#------------------------------------------------------------------

class Widget(object):
# Widget class for all widgets,  its  function is mainly to hold the
# dictionary of all widget objects by name as well as the application
# specific handler function. And support isclicked to
# see if cursor is clicked over widget.

    widgetlist = {} # dictionary of tubles of (button_object,app_handler)
    background_color = LIGHTGREY

    def __init__(self):
    # set up default dimensions in case they are not defined in
    # inherited class, this causes isclicked to default to False
        self.left = -1
        self.width = -1
        self.top = -1
        self.height = -1

    def find_widget(widget_name):
    # find the object handle for a widget by name        
        if widget_name in Widget.widgetlist:
            widget_object = Widget.widgetlist[widget_name][0]
            return  widget_object
        else:
            Print ('Error in find_widget, Widget not found ' + widget_name)
            return

    def isclicked (self, curpos):
    # button was clicked, is this the one? curpos is position tuple (x,y)
        

        covered = False

        if (curpos[0] >= self.left and
        curpos[0] <= self.left+self.width and
        curpos[1] >= self.top and
        curpos[1] <= self.top + self.height):
            covered = True

        return covered
    

    def handler(self):
    # prototype for a widget handler to be overridden if desired
        pass #do nothing    
class Text(Widget):

    def __init__(self,window=windowSurface,
                 color=BLACK,background_color=Widget.background_color,
                 topleft=(200,200),name= '',
                 font_size=20,max_chars=20,text='',
                 outline=True,outline_width=1,
                 justify = 'LEFT',
                 app_handler=Widget.handler):

        
        # initialize the properties
        self.window=window
        self.color= color
        self.background_color = background_color
        self.name = name
        self.font_size = font_size
        self.max_chars = max_chars
        self.text = text
        self.outline = outline
        self.outline_width = outline_width
        self.justify = justify
        self.app_handler = app_handler
        
        self.topleft=topleft
        self.left=topleft[0]    # reguired by isclicked method in Widget
        self.top=topleft[1]     # "
        
        # render a maximum size string to set size of text rectangle
        max_string = ''
        for i in range(0,max_chars):
            max_string += 'D'

        maxFont = pygame.font.SysFont(None,font_size)
        maxtext = maxFont.render(max_string,True,color)
        maxRect= maxtext.get_rect()
        maxRect.left = self.left
        maxRect.top = self.top
        self.maxRect = maxRect  # save for other references
        self.maxFont = maxFont

        # now set the rest required by isclicked method
        self.width = maxRect.right - maxRect.left
        self.height = maxRect.bottom -  maxRect.top


        # Add widget object keyed by name to widget dictionary.
        # Non-null Widget names must be unique.
        
        if ( (name != '') and (name not in Widget.widgetlist) ):
            Widget.widgetlist[name] = (self,app_handler)
        elif (name != ''):
            print ('Error - duplicate widget name of ' + name)

        self.draw()  # invoke the method to do the draw

        return   # end of Text initializer

    # Text method to draw the text and any outline on to the screen
    def draw(self):
        # fill the maxRect to background color to wipe any prev text
        pygame.draw.rect(self.window,self.background_color,
                         (self.maxRect.left,self.maxRect.top,
                          self.width, self.height),0)

        # if outline is requested, draw the outline 4 pixels bigger than
        # max text.  Reference topleft stays as specified
        
        if self.outline:
            pygame.draw.rect(self.window,self.color,
                             (self.maxRect.left-self.outline_width-2,
                              self.maxRect.top-self.outline_width-2,
                              self.width+(2*self.outline_width)+2,
                              self.height+(2*self.outline_width)+2),
                              self.outline_width)


        # Now put the requested text within maximum rectangle
        plottext = self.maxFont.render(self.text,True,self.color)
        plotRect = plottext.get_rect()

        plotRect.top = self.top # top doesn't move with justify

        # justify the text
        if self.justify == 'CENTER':
            plotRect.left = self.left + int(plotRect.width/2) 
        elif self.justify == 'LEFT':
            plotRect.left = self.left
        elif self.justify == 'RIGHT':
            plotRect.right = self.maxRect.right
        else:
            print('Illegal justification in Text object')

        # blit the text and update screen
        self.window.blit(plottext,plotRect)

        pygame.display.update()

    # Text method to update text and redraw
    def update(self,text):
        self.text = text
        self.draw()
#-------------- end of Text widget -----------------------------------------------

#--------------------------------------------------------------------------
# Routine to output a pixel, based on a range of y values (possibly after zooming)
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
# Routine to output a pixel, based on a normalized x and y between 0 and 1
# x_value current value of x on a scale of 0 to 1
# y_value current y value to plot for this x, on a scale of 0 to 1
# color is the color
#--------------------------------------------------------------------------

def plot_normalized(x_value,y_value,color):
  
  y_norm= y_value     # normalize y to 0 to 1 range
  ypixel = int( WINDOWHEIGHT - (y_norm*WINDOWHEIGHT)) # compute ypixel
  if (ypixel <0):
    ypixel = 0
  elif (ypixel >= WINDOWHEIGHT):
    ypixel = WINDOWHEIGHT - 1

  x_norm=  x_value     # normalize x to 0 to 1 range
  xpixel = int( x_norm*WINDOWWIDTH) # compute xpixel
  if (xpixel <0):
    xpixel = 0
  elif (xpixel >= WINDOWWIDTH):
    xpixel = WINDOWWIDTH - 1
    
  pygame.draw.circle(windowSurface,color,(xpixel, ypixel), 0 )
  pygame.display.update()

  return xpixel,ypixel      # since we have it, return the pixel plotted (can be used for later line)

#--------------------------------------------------------------------------
# Routine to get the current cursor position in terms of rho and x
# returns current rho, current x
#--------------------------------------------------------------------------

def get_cursor(begin_rho,end_rho,low_x,high_x):

  xpos,ypos = pygame.mouse.get_pos()
  cur_rho = begin_rho + ((end_rho -begin_rho) ) * (xpos/WINDOWWIDTH)
  cur_x =  low_x + (high_x - low_x) * (WINDOWHEIGHT - ypos) / WINDOWHEIGHT

  print (cur_rho,cur_x)
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

  clock.color = WHITE
  clock.text = "Plotting"
  clock.draw()

  rho_inc = (end_rho - begin_rho) / WINDOWWIDTH # compute number of rho xs to plot

  num_plots = (end_rho - begin_rho) / rho_inc
  x = 0     # start at left of window
  x_delta = WINDOWWIDTH/num_plots


  rho = begin_rho

  while rho <= end_rho :


    color = [0,255,0]
    value = beg_value
    plot_count = 0      # number of points plotted for this rho
    
    for i in range(1,10000):
      value = value * rho * (1-value)
      if (value > low_value and value < high_value ):
        if color[2] <0 or color[2] > 255:
          print (color[0],color[1],color[2])
        plot (int(x) , value,low_value,high_value,color)
        plot_count = plot_count + 1

      if plot_count <  256 :  # for first 255 points, fade from green to plue

        if color[1]  > 0:
          color[1] = color[1] - 1
        if color[2] < 255:
          color[2] = color[2] + 1
   
      elif plot_count % 5 == 0:  # change the color of the plot from blue to red as more points are plotted. 

        if color[2] > 0:
          color[2] = color[2] - 1
          if color[0] < 255:
            color[0] = color[0] + 1

      if plot_count > (.75 * WINDOWHEIGHT):       # auto density to avoid white out 
        break
      elif (i > 10000) and (plot_count == 0):      # bail on completely dark rho value
        break
      
    pygame.display.update()
    pygame.event.pump()
    x = x + x_delta
    rho = rho + rho_inc

  clock.text ="Finished"
  clock.draw()
  pygame.display.update()
  return

#---------------------------------------------------------------------------------------------
# Routine to plot the basic equation of x[n+1] = rho * x[n] * (1 - x[n])
# for a given rho.
# it puts a tick on each .05 interval of x, with a longer tick at each .1 interval
#---------------------------------------------------------------------------------------------
def plot_equation(rho):

  print ('plot_equation ',rho)

  windowSurface.fill(BLACK)       # clear plot window
  pygame.display.update()
  
  x_inc = 1.0 / WINDOWWIDTH # compute x delta for each horizontal pixel

  x = 0.

  while x <= 1.:

    y = rho * x *(1 - x)
    xpixel,ypixel = plot_normalized(x,y,WHITE)

    # put a tick mark on each .1 and .05 point

    if  int (x * 1000.) % 100 == 0:
      pygame.draw.line(windowSurface,WHITE,(xpixel,ypixel),(xpixel,ypixel-20) )      
    if  int (x * 1000.) % 50 == 0:
      pygame.draw.line(windowSurface,WHITE,(xpixel,ypixel),(xpixel,ypixel-10) )
      
    x = x + x_inc

  return

# Routine to plot the locus of points during interations
# it plots a series of lines, one for each of 

def plot_locus(rho,begin_value):

  clock.text = "Plotting"  
  color = [0,255,0]
 
  x = begin_value
  y = rho * (x-x*x)
  for plot_count in range (1,1512):
    
    x_start,y_start = plot_normalized(x,y,RED)  # determine the beginning of the line

    x = y
    y = rho * (x - x*x)
    x_end,y_end = plot_normalized(x,y,BLUE)     # determine the end of the line

    pygame.draw.line(windowSurface,color,(x_start,y_start),(x_end,y_end) )  # draw a line showing the locus move
    
    clock.color = color         # update the plot progress text in the upper left hand corner
    clock.draw()
    pygame.display.update()
    pygame.event.pump()


    if plot_count <  256 :  # for first 255 points, fade from green to plue

      if color[1]  > 0:
        color[1] = color[1] - 1
      if color[2] < 255:
        color[2] = color[2] + 1
 
    elif plot_count % 5 == 0:  # change the color of the plot from blue to red as more points are plotted. 

      if color[2] > 0:
        color[2] = color[2] - 1
        if color[0] < 255:
          color[0] = color[0] + 1

    time.sleep(.01)

  clock.text = "Finished"
  clock.draw()
  pygame.display.update()
#--------------------------------------------------------------------------
# Start of Mainline code
#--------------------------------------------------------------------------

# Put the mouse instructions on the shell
print ("Left mouse button zooms in")
print ("Right mouse button zooms out")
print ("Center mouse button plots locus of interations")
print ("Click center mouse button again to return to fractal plot")

# Set up the default variables

begin_value = .5
zoom_ratio = 4.
begin_rho = 3.5

end_rho = 4.0
low_x = 0.
high_x = 1.

# This defines the text block on the plots that shows the status of the plot
clock = Text(color=WHITE,background_color=BLACK,topleft=(10,10),
              name='clock',font_size=40,max_chars=10,text='Plotting',  
              justify='LEFT',outline=False)

plot_population(begin_value,begin_rho,end_rho,low_x,high_x) # do the fractal plot

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

    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:  # middle button is number 2, plot locus
        cur_rho, cur_x = get_cursor(begin_rho,end_rho,low_x,high_x)
        plot_equation(cur_rho)
        plot_locus(cur_rho,begin_value)

        # hang in a loop until middle button is pressed again or Quit is indicated,  then return to normal plot
        finished = False
        while not finished:

          for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:  # middle button is number 2, return to normal plot
                plot_population(begin_value,begin_rho,end_rho,low_x,high_x)
                finished = True
        
            
  time.sleep(1.)


#sys.exit
