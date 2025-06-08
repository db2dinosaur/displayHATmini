# graphical red, orangle, green meter
# supports values from 0 to "maxvalue"
# positioned on the screen with top left point (topleftx,toplefty)
# currently element widths are hard coded as elwidth=10
# element heights are set by elheight. 5 = single line of text with default_font
# label is applied to the right hand end of the meter
# a percentage of maxvalue is shown
# the value is also shown
# can set the thresholds for the different banding
#  0     >= x <= red 
#  red    > x <= orange
#  orange > x <  maxvalue = green
# We make use of PIL (pillow) to draw images on a DisplayHatMini on a Pi Zero 2W.
# The "draw" object is defined as:
#   from displayhatmini import DisplayHATMini
#   from PIL import Image, ImageDraw, ImageFont
#   width = DisplayHATMini.WIDTH
#   height = DisplayHATMini.HEIGHT
#   buffer = Image.new("RGB",(width,height))
#   draw = ImageDraw.Draw(buffer)
#   displayhatmini = DisplayHATMini(buffer)
#
# The init parms are:
# + draw = PIL image draw object on a pre-defined buffer set against the DisplayHATMini (see above)
# + topleftx = the "x" part of the top left point that we're drawing from
# + toplefty = the "y" part of the top left point that we're drawing from
# + elheight = the tick element height on the meter
# + initvalue = the initial value to show on the meter
# + maxvalue = the maximum value for the meter (@ 100%)
# + label = a text label for the meter
# + (optional) red = the upper percentage boundary of the red part of the meter - default = 15
# + (optional) orange = the upper percentage boundary of the orange part of the meter - default = 45
#
# JG 2025-04-21
from PIL import Image, ImageDraw, ImageFont

class Meter:
    def __init__(self,draw,displayWidth,topleftx,toplefty,elheight,initvalue, maxvalue, label, red=15, orange=45):
#        global draw
        self.draw = draw
        self.displayWidth = displayWidth
        self.position = (topleftx, toplefty)
        self.elheight = elheight
        self.value = initvalue
        self.max = maxvalue
        self.label = label
        self.red = red
        self.orange = orange

    @property
    def topleftx(self):
        return self.position[0]
    
    @property
    def toplefty(self):
        return self.position[1]

    def setval(self,newvalue):
        self.value = newvalue
        if self.value > self.max:
            self.value = self.max
        if self.value < 0:
            self.value = 0

    def wipe(self):
        self.draw.rectangle((self.topleftx,self.toplefty,self.displayWidth,self.toplefty),(0,0,0))

    def drawText(self,draw,text,position,size,colour):
        fnt = ImageFont.load_default()
        x1y1x2y2 = fnt.getbbox(text)
        draw.text(position,text,font=fnt,fill=colour)
        return x1y1x2y2

    def update(self):
        val = self.value
        max = self.max
        elwidth = 10
        elppad = elwidth + 2
        pct = (float(val) / float(max)) * 100
        self.wipe()
        for i in range(20):
            x1 = (i * elppad) + self.topleftx
            x2 = x1 + elwidth
            colour = (0,0,0)
            ipct = (float(i) / float(20)) * 100
            if ipct <= pct:
                if ipct <= self.red:
                    colour = (240,0,0)
                elif ipct > self.red and ipct < self.orange:
                    colour = (240,180,0)
                elif ipct >= self.orange:
                    colour = (0,240,0)
            self.draw.rounded_rectangle(((x1,self.toplefty),(x2,self.toplefty + self.elheight)),radius=2,fill=colour)
        txtx = self.topleftx + (20 * elppad)
        # Add label to end of meter
        box = self.drawText(self.draw,self.label,(txtx,self.toplefty),24,(240,240,0))
        # Report value
        txty = self.toplefty + box[3]  # x1,y1,x2,y2
        box = self.drawText(self.draw,"Val: {0:d}".format(self.value),(txtx,txty),24,(240,240,0))
        # Report pct
        txty += box[3]
        box = self.drawText(self.draw,"Pct: {0:02.2f}%".format(pct),(txtx,self.toplefty + 20),24,(240,240,0))
