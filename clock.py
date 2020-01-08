import pygame
from datetime import datetime
import time
from pygame.locals import *
from pygame.compat import unichr_, unicode_
import sys
import locale

#Initialize pygame
pygame.init()


def processEvents():
    global done, military, font

    #retrieve event queue
    events = pygame.event.get()

    #loop through event queue
    for event in events:

        #close window on quit event
        if event.type == pygame.QUIT:
            done = True

        #process key presses
        if event.type == pygame.KEYDOWN:

            #close window on esc pressed
            if event.key ==  pygame.K_ESCAPE:
                done = True
            #switch between military and AM/PM notation on tab pressed
            if event.key == pygame.K_TAB:
                military = not military
                font = pygame.font.Font('Roboto_Mono\\RobotoMono-Bold.ttf', int(resolution[0]/(5-(military)*2)))

               
def update():
    global resolution, font, military
    
    #fill background
    screen.fill(wincolor)
    
    #Query System time
    t = datetime.today()
    
    #Create time string
    time = ''
    
    #Add hours to time string
    if t.hour%(12+(military)*12) < 10:
        time += '0'+str(t.hour%(12+(military)*12))
    else:
        time += str(t.hour%(12+(military)*12))
        
    #Add Flashing colon
    if t.second%2:
        time += ':'
    else:
        time += ' '
        
    #Add minutes to time string
    if t.minute < 10:
        time += '0'+str(t.minute)
    else:
        time += str(t.minute)
    #If using 12-hour clock, append AM/PM
    if not military:   
        if t.hour > 12:
            time += ' PM'
        else:
            time += ' AM'
    
    
    #Create render of time
    timeRen = font.render(time, 1, fg, bg)
    
    screen.blit(timeRen,(int((resolution[0]-timeRen.get_width())/2), (int((resolution[1]-timeRen.get_height())/32)-66)))

#retrieve screen size information
monitorInfo = pygame.display.Info()

#globals
global fg, bg, wincolor
global resolution
global font
global done
global fps
global military

#globals initialization
fg = 250, 240, 230
bg = 5, 5, 5
wincolor = 5, 5, 5
resolution = monitorInfo.current_w,monitorInfo.current_h
font = pygame.font.Font('Roboto_Mono\\RobotoMono-Bold.ttf', int(resolution[0]/5))
font.set_bold(1)
done = False
fps = 20
military = False

#initialize window
screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)

lastTime = 0.0

#main loop
while not done:

    #process keyboard and mouse events
    processEvents()

    #update screen
    update()
    pygame.display.flip()

    #limit fps to save resources
    tdif = time.time()-lastTime
    time.sleep(max(0,1.0/fps-tdif))
    lastTime = time.time()
    
    

pygame.display.quit()
