# Produce an updating trace on a Pi Zero2 with a DisplayHatMini installed. This allows us
# to provide a continuous update view of our data.
#
# We will need to know:
# * Width of display area
# * Height of display area
# * Min and Max values
# * Chart title
# * Label for legend showing current value
# 
# Values will be held in a list. Each time that we get told about a new value, it will be added
# to the end of the list, and if this makes us bigger than the max list size, we'll drop the
# oldest entry.
#


class Scope:
    def __init__(self,draw,topleftx,toplefty,width,height,buffsize=200,initval=0,max=100,min=0):
        self.max = max
        self.min = min
        self.buffsize = buffsize
        self.cbfsize = 0
        self.valbuf = []
        self._value = min
        self.value = initval
        self.topleft = (topleftx, toplefty)
        self.bottomright = (topleftx + width, toplefty + height)
        self.draw = draw
        self.xratio = float(width) / buffsize
        self.yratio = float(height) / (max - min)
        self.y0 = self.bottomright[1] - int(abs(self.min) * self.yratio)
        print("DEBUG: %d,%d - %d,%d" % (width,height,self.topleft[0],self.y0))
        self.debug()
    
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self,newvalue):
        xx = newvalue
        if xx > self.max:
            xx = self.max
        elif xx < self.min:
            xx = self.min
        self._value = xx
        self.valbuf.append(xx)
        self.cbfsize = self.cbfsize + 1
        if self.cbfsize > self.buffsize:
            self.valbuf.pop(0)
            self.cbfsize = self.cbfsize - 1
    
    def debug(self):
        print("DEBUG: max(%d) min(%d) buffsize(%d) cbfsize(%d) lastval(%f)" % (self.max,self.min,self.buffsize,self.cbfsize,self.value))
        print(self.valbuf)

    def clear(self):
        self.draw.rectangle([self.topleft,self.bottomright],(0,0,0))
    
    # min to max maps to bottomrighty (bottomright[1]) to toplefty (topleft[1])
    # x0 to xlast (0 to buffsize) maps to topleftx (topleft[0]) to bottomrightx (bottomright[0])
    def update(self):
        # assemble coords for scope trace
        xylist = []
        x = 0
        for v in self.valbuf:
            thisx = int(x * self.xratio) + self.topleft[0]
            thisy = self.bottomright[1] - int((v - self.min) * self.yratio)
            coord = (thisx,thisy)
            xylist.append(coord)
            x = x + 1
        # draw the axes
        self.draw.line([self.topleft,(self.topleft[0],self.bottomright[1])],fill=(20,240,20),width=1)
        self.draw.line([(self.topleft[0],self.y0),(self.bottomright[0],self.y0)],fill=(20,240,20),width=1)
        # draw the line
        self.draw.line(xylist,fill=(240,240,80),width=1)
