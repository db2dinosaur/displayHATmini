# Drive the display hat mini with the Scope class to validate
#
import time
from datetime import datetime
import math
import numpy as np
import threading
from collections import namedtuple
from displayhatmini import DisplayHATMini
try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("""This code requires PIL/Pillow, try:
    
1. If in venv :    pip3 install pillow 
2. If not     :    sudo apt install python3-pil
""")
import Scope

width = DisplayHATMini.WIDTH
height = DisplayHATMini.HEIGHT
print("DEBUG: Width=%d, Height=%d" % (width,height))
buffer = Image.new("RGB",(width,height))
draw = ImageDraw.Draw(buffer)
displayhatmini = DisplayHATMini(buffer)
displayhatmini.set_led(0,0,0)
Position = namedtuple('Position', 'x y')
Size = namedtuple('Size', 'w h')

def clear(draw,w,h):
    draw.rectangle((0,0,w,h),(0,0,0))

def text(draw,text,position,size,colour):
    fnt = ImageFont.load_default()
    draw.text(position,text,font=fnt,fill=colour)

val = 0
maxval = 75
killed = False
dead = False
def ticktock():
    global val, maxval, dead
    twopi = 2 * np.pi
    tick = twopi / 50
    while not killed:
        for i in range(0,50):
            val = int(maxval * ((np.sin(float(i) * tick))/2.0))
            time.sleep(0.05)
    dead = True

timerThread = threading.Thread(target=ticktock)
timerThread.daemon = True
timerThread.start()

done = False
# Scope init parms:
#  pillow.draw, topleftx,toplefy,width,height
s = Scope.Scope(draw,5,20,width - 10,height - 40,buffsize=100,initval=0,max=100,min=-100)
last_pushed = 0
while not done:
    add = ""
    this_push = 0
    clear(draw,width,height)
    tsnow = datetime.now()
    txt = "Latest sample at %04d-%02d-%02d %02d:%02d:%02d.%06d" % (tsnow.year,tsnow.month,tsnow.day,tsnow.hour,tsnow.minute,tsnow.second,tsnow.microsecond)
    text(draw,txt,(0,0),24,(255,255,255))
    if displayhatmini.read_button(displayhatmini.BUTTON_A):
        this_push += 1
    if displayhatmini.read_button(displayhatmini.BUTTON_B):
        this_push += 2
    if displayhatmini.read_button(displayhatmini.BUTTON_X):
        this_push += 4
    if displayhatmini.read_button(displayhatmini.BUTTON_Y):
        this_push += 8
    pushed = last_pushed ^ this_push
    s.value = val
    s.update()
    displayhatmini.display()
    last_pushed = this_push
    # if all 4 buttons are pushed
    if last_pushed == 15:
        displayhatmini.set_led(0,0,0)

        killed = True
        done = True
        q = 0
        while not dead:
            q += 1
            time.sleep(0.05)
        # really really wait for the thread to end
        timerThread.join()
        print("Spin for %dms waiting to end" % (q * 5))
    time.sleep(0.001)
