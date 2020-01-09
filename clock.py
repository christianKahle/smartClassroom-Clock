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
    global done, military, font, scrollSpeed

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

            # change scroll speed with UP / DOWN
            if event.key == pygame.K_UP:
                scrollSpeed += 5
            if event.key == pygame.K_DOWN:
                scrollSpeed -= 5


               
def update():
    #Query System time
    today = datetime.today()

    #fill background
    screen.fill(wincolor)

    announce()
    clock()
    


def clock():
    global resolution, font, military, today
    
    #Create time string
    time = ''
    
    #Add hours to time string
    if today.hour%(12+(military)*12) < 10:
        time += '0'+str(today.hour%(12+(military)*12))
    else:
        time += str(today.hour%(12+(military)*12))
        
    #Add Flashing colon
    if today.second%2:
        time += ':'
    else:
        time += ' '
        
    #Add minutes to time string
    if today.minute < 10:
        time += '0'+str(today.minute)
    else:
        time += str(today.minute)
    #If using 12-hour clock, append AM/PM
    if not military:   
        if today.hour > 12:
            time += ' PM'
        else:
            time += ' AM'

    
    #Create render of time
    timeRen = timeFont.render(time, 1, fg, bg)
    
    # place render on screen
    screen.blit(timeRen,(int((resolution[0]-timeRen.get_width())/2), (int((resolution[1]-timeRen.get_height())/32)-66)))

def announce():
    global font, resolution, scrollSpeed, offset
    
    #open announcement file
    announcement = open("announcement.txt","r")

    text = announcement.read()
    #read file and render each line
    offset -= scrollSpeed
    for c in text:
        offset = (offset+font.size(c)[0])%font.size(text)[0]
        
        announceRen = font.render(c, 1, fg, bg)
        screen.blit(announceRen,(offset,(int((resolution[1]-announceRen.get_height())/32)-66+int(timeFont.size('1')[1]*.75))))
    
    announcement.close()




#retrieve screen size information
monitorInfo = pygame.display.Info()

#globals
global fg, bg, wincolor
global resolution
global font, timeFont
global done
global fps
global military
global today
global scrollSpeed
global offset

#globals initialization
fg = 250, 240, 230
bg = 5, 5, 5
wincolor = 5, 5, 5
resolution = monitorInfo.current_w,monitorInfo.current_h
timeFont = pygame.font.Font('Roboto_Mono\\RobotoMono-Bold.ttf', int(resolution[0]/5))
font = pygame.font.Font('Roboto_Mono\\RobotoMono-Bold.ttf', int(resolution[0]/3))
font.set_bold(1)
done = False
fps = 20
military = False
today = datetime.today()
scrollSpeed = 25
offset = 0

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
