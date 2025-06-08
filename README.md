# displayHATmini
This code is a work in progress to develop some different ways of presenting state data using a Raspberry Pi Zero 2W with a DisplayHATMini installed. This is a small format colour LCD display that fits onto the headers for the Pi Zero.

* DisplayHATMini reference here: https://github.com/pimoroni/displayhatmini-python/tree/main/library/displayhatmini
* st7789 (controller on the DHM) here: https://github.com/pimoroni/st7789-python/blob/main/examples/image.py
* Python Image Library (pillow fork) here: https://github.com/python-pillow/Pillow

A couple of Classes and examples to drive them:

* Meter - produces a VU meter style current-value display with coloured output (red, orange, green) with configurable threasholds. Handy for "what's happening right now" displays
* Scope - a value trace, a bit like an oscillascope. More useful for "what has been happening up until now" displays.

These are driven by sine waves by two driving apps:

* dhmini.py - as well as showing the Meter class, this also demonstrates use of the LED and buttons on the DHM
* scopetest.py - shows off the Scope class.

Both of these examples can be cleanly shutdown by pressing all four buttons on the DHM at the same time.

JG 2025/06/08
