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
    global done, military, scrollSpeed, leadZero

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
                scrollSpeed += .25
            if event.key == pygame.K_DOWN:
                scrollSpeed -= .25
            if event.key == pygame.K_z:
                leadZero = not leadZero


               
def update():
    global today
    if today.minute%30 == 0:
        updateMessage()
    #Query System time
    today = datetime.today()

    #fill background
    screen.fill(wincolor)

    announce()
    clock()
    


def clock():
    global resolution, font, military, today, leadZero
    
    #Create time string
    time = ''
    
    #Add hours to time string
    if today.hour%(12+(military)*12) < 10 and leadZero:
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
    timeRen = font.render(time, 1, fg, bg)
    
    # place render on screen
    screen.blit(timeRen,(int((resolution[0]-timeRen.get_width())/2), 0))

def announce():
    global font, resolution, scrollSpeed, offset, fps, chSize, announcement, textLength
    
    #open announcement file
    
    #read file and render each line
    offset -= int(scrollSpeed*resolution[0]/fps)
    for c in announcement:

        offset += chSize[0]
        if offset > textLength:
            offset %= textLength

        if c != ' ' and offset-chSize[0] < resolution[0]:
            announceRen = font.render(c, 1, fg, bg)
            screen.blit(announceRen,(offset-chSize[0],int(font.size(' ')[1])))

def updateMessage():
    global announcement, textLength
    a = open("announcement.txt","r")
    announcement = a.read()+'      '
    a.close()

    textLength = font.size(announcement)[0]

#retrieve screen size information
monitorInfo = pygame.display.Info()

#globals
global fg, bg, wincolor
global resolution
global font
global done
global fps
global military, leadZero
global today
global scrollSpeed
global chSize
global offset
global announcement
global textLength

#globals initialization
fg = 250, 240, 230
bg = 5, 5, 5
wincolor = 5, 5, 5
resolution = monitorInfo.current_w,monitorInfo.current_h
font = pygame.font.Font('Roboto_Mono\\RobotoMono-Bold.ttf', int(resolution[0]/5))
font.set_bold(1)
done = False
fps = 60
military = False
leadZero = True
today = datetime.today()
scrollSpeed =  1 #screens per second
chSize = font.size(' ')
offset = int(resolution[0]/2)
updateMessage()

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
