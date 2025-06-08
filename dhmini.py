# Python code to pull the current weather info from the interweb and
# display it on the DisplayHatMini (320 x 200).
#
import time
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
import Meter

width = DisplayHATMini.WIDTH
height = DisplayHATMini.HEIGHT
buffer = Image.new("RGB",(width,height))
draw = ImageDraw.Draw(buffer)
displayhatmini = DisplayHATMini(buffer)
displayhatmini.set_led(0.05,0.05,0.05)
Position = namedtuple('Position', 'x y')
Size = namedtuple('Size', 'w h')

def clear(draw,w,h):
    draw.rectangle((0,0,w,h),(0,0,0))

def text(draw,text,position,size,colour):
    fnt = ImageFont.load_default()
    draw.text(position,text,font=fnt,fill=colour)

# # graphical red, orangle, green meter
# # supports values from 0 to "maxvalue"
# # positioned on the screen with top left point (topleftx,toplefty)
# # currently element widths are hard coded as elwidth=10
# # element heights are set by elheight. 5 = single line of text with default_font
# # label is applied to the right hand end of the meter
# # a percentage of maxvalue is show
# # the value is also shown
# # can set the thresholds for the different banding
# #  0     >= x <= red 
# #  red    > x <= orange
# #  orange > x <  maxvalue = green
# class Meter():
#     def __init__(self,topleftx,toplefty,elheight,initvalue, maxvalue, label, red=15, orange=45):
#         global draw
#         self.position = (topleftx, toplefty)
#         self.elheight = elheight
#         self.value = initvalue
#         self.max = maxvalue
#         self.label = label
#         self.red = red
#         self.orange = orange

#     @property
#     def topleftx(self):
#         return self.position[0]
    
#     @property
#     def toplefty(self):
#         return self.position[1]

#     def setval(self,newvalue):
#         self.value = newvalue
#         if self.value > self.max:
#             self.value = self.max
#         if self.value < 0:
#             self.value = 0

#     def wipe(self):
#         draw.rectangle((self.topleftx,self.toplefty,width,self.toplefty),(0,0,0))

#     def drawText(self,draw,text,position,size,colour):
#         fnt = ImageFont.load_default()
#         x1y1x2y2 = fnt.getbbox(text)
#         draw.text(position,text,font=fnt,fill=colour)
#         return x1y1x2y2

#     def update(self):
#         val = self.value
#         max = self.max
#         elwidth = 10
#         elppad = elwidth + 2
#         pct = (float(val) / float(max)) * 100
#         self.wipe()
#         for i in range(20):
#             x1 = (i * elppad) + self.topleftx
#             x2 = x1 + elwidth
#             colour = (0,0,0)
#             ipct = (float(i) / float(20)) * 100
#             if ipct <= pct:
#                 if ipct <= self.red:
#                     colour = (240,0,0)
#                 elif ipct > self.red and ipct < self.orange:
#                     colour = (240,180,0)
#                 elif ipct >= self.orange:
#                     colour = (0,240,0)
#             draw.rounded_rectangle(((x1,self.toplefty),(x2,self.toplefty + self.elheight)),radius=2,fill=colour)
#         txtx = self.topleftx + (20 * elppad)
#         # Add label to end of meter
#         box = self.drawText(draw,self.label,(txtx,self.toplefty),24,(240,240,0))
#         # Report value
#         txty = self.toplefty + box[3]  # x1,y1,x2,y2
#         box = self.drawText(draw,"Val: {0:d}".format(self.value),(txtx,txty),24,(240,240,0))
#         # Report pct
#         txty += box[3]
#         box = self.drawText(draw,"Pct: {0:02.2f}%".format(pct),(txtx,self.toplefty + 20),24,(240,240,0))

val = 0
maxval = 57
killed = False
dead = False
def ticktock():
    global val, maxval, dead
    twopi = 2 * np.pi
    tick = twopi / 1000
    while not killed:
        for i in range(0,1000):
            val = int(maxval * ((1.0 + np.sin(float(i) * tick))/2.0))
            time.sleep(0.005)
    dead = True

timerThread = threading.Thread(target=ticktock)
timerThread.daemon = True
timerThread.start()

done = False
# Meter(x,y,height,value,max,label)
vu = Meter.Meter(draw,width,5,100,22,val,maxval,"VU Meter")
# buttons are not enumerated in the class, so:
#   None = 0, A = 1, B = 2, X = 4, Y = 8
last_pushed = 0
while not done:
    add = ""
    this_push = 0
    clear(draw,width,height)
    text(draw,"It's a curious thing, this, but it seems to work!",(25,25),24,(255,255,255))
    ledR = 0
    ledG = 0
    ledB = 0
    if displayhatmini.read_button(displayhatmini.BUTTON_A):
        add += "A "
        this_push += 1
        ledR = 0.2
    if displayhatmini.read_button(displayhatmini.BUTTON_B):
        add += "B "
        this_push += 2
        ledB = 0.2
    if displayhatmini.read_button(displayhatmini.BUTTON_X):
        add += "X "
        this_push += 4
        ledG = 0.2
    if displayhatmini.read_button(displayhatmini.BUTTON_Y):
        add += "Y "
        this_push += 8
    displayhatmini.set_led(ledR,ledG,ledB)
    text(draw,add,(24,50),24,(255,255,255))
    pushed = last_pushed ^ this_push
    # what's been pushed since the last loop? Handy for push transition
    if (pushed & 1) > 0 and (this_push & 1) > 0:
        val = val + 5
    if (pushed & 2) > 0 and (this_push & 2) > 0:
        val = val - 5
    if (pushed & 4) > 0 and (this_push & 4) > 0:
        val = val + 1
    if (pushed & 8) > 0 and (this_push & 8) > 0:
        val = val - 1
    # what's been released since the last loop? Handy for release transition
    if (pushed & 1) > 0 and (this_push & 1) == 0:
        q = 0
    if (pushed & 2) > 0 and (this_push & 2) == 0:
        q = 1
    if (pushed & 4) > 0 and (this_push & 4) == 0:
        q = 2
    if (pushed & 8) > 0 and (this_push & 8) == 0:
        q = 3
    vu.setval(val)
    vu.update()
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
