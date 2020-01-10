import pygame
from datetime import datetime
import time
from pygame.locals import *
from pygame.compat import unichr_, unicode_
import sys
import locale
import re

#Initialize pygame
pygame.init()


def processEvents():
    global done, military, scrollSpeed, leadZero, offset, scroll, wait

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
            #toggle leading hour zero with Z
            if event.key == pygame.K_z:
                leadZero = not leadZero
            #toggle text scrolling / switching with S
            if event.key == pygame.K_s:
                if scroll:
                    wait = time.time()+len(words[0])/scrollSpeed/15
                scroll = not scroll
                offset = 0


               
def update():
    global today, pendingMessageUpdate
    if today.minute == 0:
        if pendingMessageUpdate:
            updateMessage()
        pendingMessageUpdate = False
    else:
        pendingMessageUpdate = True
    #Query System time
    today = datetime.today()

    #fill background
    screen.fill(wincolor)

    if scroll:
        announce()
    else:
        quickAnnounce()

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
    timeRen = timeFont.render(time, 1, fg, bg)
    
    # place render on screen
    screen.blit(timeRen,(int((resolution[0]-timeRen.get_width())/2), 0))

def announce():
    global font, resolution, scrollSpeed, offset, fps, chSize, tchSize, announcement, textLength

    #change offset every frame to scroll text
    offset -= int(scrollSpeed*resolution[0]/fps)

    #loop through each character
    for c in announcement:

        offset += chSize[0]
        if offset > textLength:
            offset %= textLength

        if c != ' ' and offset-chSize[0] < resolution[0]:
            announceRen = font.render(c, 1, fg, bg)
            screen.blit(announceRen,(offset-chSize[0],tchSize[1]))
        
def quickAnnounce():
    global font, resolution, words, offset, frame, wait, scrollSpeed, fontFile
    if time.time() > wait:
        offset = (offset+1)%(len(words))
        wait = time.time()+len(words[offset])/scrollSpeed/15
    
    announceRen = font.render(words[offset], 1, fg, bg)
    if announceRen.get_width() > resolution[0]:
        font = pygame.font.Font(fontFile, int(resolution[0]/6*resolution[0]/announceRen.get_width()))
        announceRen = font.render(words[offset], 1, fg, bg)
        screen.blit(announceRen,(int((resolution[0]-announceRen.get_width())/2),tchSize[1]+(chSize[1]-announceRen.get_height())/2))
        font = pygame.font.Font(fontFile, int(resolution[0]/6))
    else:
        screen.blit(announceRen,(int((resolution[0]-announceRen.get_width())/2),tchSize[1]))
    

def updateMessage():
    global announcement, textLength, offset, words
    #open announcement file
    a = open("announcement.txt","r")
    # save text to string
    announcement = a.read()+'      '
    #close announcement file
    a.close()

    #calculate pixel length of text
    textLength = font.size(announcement)[0]

    #reset to beginning of message
    offset = 0

    #create list of each word
    words = [word for word in re.split('[ \n]+',announcement)]
    words += ['          ']
    

#retrieve screen size information
monitorInfo = pygame.display.Info()

#globals
global fontFile
global fg, bg, wincolor
global resolution
global font, timeFont
global done
global fps
global military, leadZero
global today
global scrollSpeed
global scroll
global chSize, tchSize
global offset
global announcement, words
global textLength
global pendingMessageUpdate
global wait

#globals initialization
fontFile = 'Roboto_Mono/RobotoMono-Bold.ttf'
fg = 250, 240, 230
bg = 5, 5, 5
wincolor = 5, 5, 5
resolution = monitorInfo.current_w,monitorInfo.current_h
timeFont = pygame.font.Font(fontFile, int(resolution[0]/5))
font = pygame.font.Font(fontFile, int(resolution[0]/6))
font.set_bold(1)
done = False
fps = 60
military = False
leadZero = True
today = datetime.today()
scrollSpeed =  1 #screens per second
scroll = True
chSize = font.size(' ')
tchSize = timeFont.size(' ')
offset = int(resolution[0]/2)
updateMessage()
pendingMessageUpdate = False
wait = time.time()+len(words[0])/scrollSpeed/15

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
