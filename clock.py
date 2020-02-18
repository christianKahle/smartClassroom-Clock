import pygame
from datetime import *
from schedule import *
import time
from pygame.locals import *
from pygame.compat import unichr_, unicode_
import sys , locale, os, re
import configparser

#Initialize pygame
pygame.init()

def processEvents():
    global done, military, scrollSpeed, leadZero, offset, scroll, wait, display, showing_schedule

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
                scrollSpeed += .1
            if event.key == pygame.K_DOWN:
                if scrollSpeed != .1:
                    scrollSpeed -= .1
            #toggle leading hour zero with Z
            if event.key == pygame.K_z:
                leadZero = not leadZero
            #toggle text scrolling / switching with S
            if event.key == pygame.K_s:
                if scroll:
                    wait = time.time()+len(words[0])/scrollSpeed/15
                scroll = not scroll
                offset = 0
            if event.key == K_f:
                if display == clock:
                    display = fire_drill
                else:
                    display = clock
                offset = -30
            if event.key == K_g:
                if display == clock:
                    display = fire_alarm
                else:
                    display = clock
            if event.key == K_t:
                if display == clock:
                    display = tornado_drill
                else:
                    display = clock
            if event.key == K_y:
                if display == clock:
                    display = tornado_alarm
                else:
                    display = clock
            if event.key == K_l:
                if display == clock:
                    display = lockdown_drill
                else:
                    display = clock
            if event.key == K_l:
                if display == clock:
                    display = lockdown_alarm
                else:
                    display = clock
            if event.key == K_s:
                showing_schedule = not showing_schedule
               
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

    display()
    
def fire_drill():
    global dcolor, bg
    screen.fill(dcolor)
    message = "This is a FIRE DRILL. Please evacuate according to your instructions. "
    announce_FS(bg, dcolor,message,1.25)
def tornado_drill():
    global dcolor, bg
    screen.fill(dcolor)
    message = "This is a TORNADO DRILL. Please take shelter according to your instructions. "
    announce_FS(bg, dcolor,message,1.25)
def lockdown_drill():
    global dcolor, bg
    screen.fill(dcolor)
    message = "This is a LOCKDOWN DRILL. Please take shelter according to your instructions. "
    announce_FS(bg, dcolor,message,1.25)

def fire_alarm():
    global ecolor, bg
    screen.fill(ecolor)
    message = "This is a FIRE ALARM. Please evacuate according to your instructions. "
    announce_FS(bg, ecolor,message,1.25)
def tornado_alarm():
    global ecolor, bg
    screen.fill(ecolor)
    message = "This is a TORNADO ALARM. Please take shelter according to your instructions. "
    announce_FS(bg, ecolor,message,1.25)
def lockdown_alarm():
    global ecolor, bg
    screen.fill(ecolor)
    message = "This is a LOCKDOWN ALARM. Please take shelter according to your instructions. "
    announce_FS(bg, ecolor,message,1.25)

def clock():
    global resolution, font, military, today, leadZero, tcolor, acolor, bg
    screen.fill(bg)
    if showing_schedule:
        showSchedule()
    else:
        if scroll:
            announce(acolor)
        else:
            quickAnnounce(acolor)
        
    
    #Create time string
    time = ''
    
    #Add hours to time string
    hours = 12*(1+military)
    time += '0'*(leadZero and today.hour%hours<10)+str((today.hour-1)%hours+1)
        
    #Add Flashing colon
    time+= ':'*(today.second%2)+' '*((today.second+1)%2)
        
    #Add minutes to time string
    time += '0'*(today.minute<10)+str(today.minute)

    #If using 12-hour clock, append AM/PM
    time += (' '+chr(65+15*(today.hour > 11))+'M')*(not military)

    #Create render of time
    timeRen = timeFont.render(time, 1, tcolor, bg)
    
    # place render on screen
    screen.blit(timeRen,(int((resolution[0]-timeRen.get_width())/2), 0))

def announce(color):
    global font, resolution, scrollSpeed, offset, fps, chSize, tchSize, textLength, announcement

    #change offset every frame to scroll text
    offset -= int(scrollSpeed*resolution[0]/fps)

    #loop through each character
    for c in announcement:

        offset += chSize[0]
        offset %= textLength

        if c != ' ' and offset-chSize[0] < resolution[0]:
            announceRen = font.render(c, 1, color, bg)
            screen.blit(announceRen,(offset-chSize[0],tchSize[1]))

def announce_FS(color, background_color,announcement,speedmult = 1):
    global fullFont, resolution, scrollSpeed, offset, fps
    #change offset every frame to scroll text
    offset -= int(scrollSpeed*speedmult*resolution[0]/fps)

    #loop through each character
    for c in announcement:

        offset += fullFont.size(" ")[0]
        offset %= fullFont.size(announcement)[0]

        if c != ' ' and offset-fullFont.size(" ")[0] < resolution[0]:
            announceRen = fullFont.render(c, 1, color, background_color)
            screen.blit(announceRen,(offset-fullFont.size(" ")[0],int(resolution[1]/8)))

def quickAnnounce(color):
    global font, resolution, words, offset, frame, wait, scrollSpeed, fontFile
    if time.time() > wait:
        offset = (offset+1)%(len(words))
        wait = time.time()+len(words[offset])/scrollSpeed/15
    
    announceRen = font.render(words[offset], 1, acolor, bg)
    if announceRen.get_width() > resolution[0]:
        font = pygame.font.Font(fontFile, int(resolution[0]/6*resolution[0]/announceRen.get_width()))
        announceRen = font.render(words[offset], 1, acolor, bg)
        screen.blit(announceRen,(int((resolution[0]-announceRen.get_width())/2),tchSize[1]+int((chSize[1]-announceRen.get_height())/2)))
        font = pygame.font.Font(fontFile, int(resolution[0]/6))
    else:
        screen.blit(announceRen,(int((resolution[0]-announceRen.get_width())/2),tchSize[1]))



def updateMessage():
    global announcement, textLength, offset, words
    #open announcement file
    a = open(os.path.join(path,'announcement.txt'),"r")
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

def showSchedule():
    global font, resolution, Schedule
    now = datetime.now().time()
    evs = Schedule.current_events(now)
    if len(evs) != 0:
        stuff = evs[0].split(',')[2]
    else:
        stuff = Schedule.next_event(now).split(',')[2]

    announceRen = font.render(stuff, 1, acolor, bg)
    if announceRen.get_width() > resolution[0]:
        font = pygame.font.Font(fontFile, int(resolution[0]/6*resolution[0]/announceRen.get_width()))
        announceRen = font.render(stuff, 1, acolor, bg)
        screen.blit(announceRen,(int((resolution[0]-announceRen.get_width())/2),tchSize[1]+int((chSize[1]-announceRen.get_height())/2)))
        font = pygame.font.Font(fontFile, int(resolution[0]/6))
    else:
        screen.blit(announceRen,(int((resolution[0]-announceRen.get_width())/2),tchSize[1]))
    
#retrieve screen size information
monitorInfo = pygame.display.Info()

#config loading and global initialization
path = os.path.dirname(__file__)
config = configparser.ConfigParser()
config.read(os.path.join(path,'config.ini'))
fontFile = os.path.join(path,'Roboto_Mono','RobotoMono-Bold.ttf')
tcolor = [int(c) for c in config['DEFAULT']['time_color'].split(',')]
acolor = [int(c) for c in config['DEFAULT']['announcement_color'].split(',')] 
bg = [int(c) for c in config['DEFAULT']['background_color'].split(',')]
dcolor = [int(c) for c in config['DEFAULT']['drill_color'].split(',')]
ecolor = [int(c) for c in config['DEFAULT']['emergency_color'].split(',')]
resolution = monitorInfo.current_w,monitorInfo.current_h
timeFont = pygame.font.Font(fontFile, int(resolution[0]/5))
font = pygame.font.Font(fontFile, int(resolution[0]/6))
fullFont = pygame.font.Font(fontFile, int(resolution[1]/2))
font.set_bold(1)
done = False
fps = int(config['DEFAULT']['frames_per_second'])
military = bool(int(config['DEFAULT']['military_time']))
leadZero = bool(int(config['DEFAULT']['leading_zero']))
today = datetime.today()
scrollSpeed =  1 #screens per second
scroll = bool(int(config['DEFAULT']['scroll_text']))
chSize = font.size(' ')
tchSize = timeFont.size(' ')
offset = int(resolution[0]/2)
words = []
updateMessage()
pendingMessageUpdate = False
wait = time.time()+len(words[0])/scrollSpeed/15
display = clock
Schedule = schedule(os.path.join(path,'Schedules.ini'),'DEFAULT')
showing_schedule = True
today = datetime.today()

#initialize window
screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)

pygame.mouse.set_visible(False)

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
    
    
pygame.mouse.set_visible(True)
pygame.display.quit()
quit()
