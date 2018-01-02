#!/usr/bin/env python
# SHFramework Provides Simple GUI management capability for nanohat on neo pi

import bakebit_128_64_oled as oled
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import threading
import signal
import abc

global SH_WIDTH
SH_WIDTH = 128
global SH_HEIGHT
SH_HEIGHT = 64
global fontb24
fontb24 = ImageFont.truetype('DejaVuSansMono-Bold.ttf', 24);
global font14 
font14 = ImageFont.truetype('DejaVuSansMono.ttf', 14);
global smartFont
smartFont = ImageFont.truetype('DejaVuSansMono-Bold.ttf', 10);
global fontb14
fontb14 = ImageFont.truetype('DejaVuSansMono-Bold.ttf', 14);
global font11
font11 = ImageFont.truetype('DejaVuSansMono.ttf', 11);

# initialize OLED display
oled.init()
oled.setNormalDisplay()
oled.setHorizontalMode()

class SHPageView(object):
    pageUDID = 0
    def __init__(self, name='View'):
        self.udid = SHPageView.pageUDID
        self.name = name
        SHPageView.pageUDID += 1

    @abc.abstractmethod
    def getImage(self):
        # Should be overridden by implementation pages
        # Here's a default implementation that could be invoked via super()
        img = Image.new('1', (SH_WIDTH, SH_HEIGHT))
        draw = ImageDraw.Draw(img)
        draw.text((2,2), 'Page '+str(self.udid), font=font14, fill=255)
        return img

    def getUDID(self):
        # UDID used as page number, ranging from [0, n)
        return self.udid

class SHController:
    pages = {}
    cntPage = 0

    @staticmethod
    def update():
        # updates screen by calling current page getImage
        page = SHController.pages[SHController.cntPage]
        img  = page.getImage()
        oled.drawImage(img)

    @staticmethod
    def btn_handler(signum, stack):
        cntPage = SHController.cntPage
        pagelen = len(SHController.pages)
        if signum == signal.SIGUSR1:
            # Key LEFT
            print 'K1 pressed'
            cntPage = (cntPage - 1) % pagelen
        elif signum == signal.SIGALRM:
            # Key RIGHT
            print 'K3 pressed'
            cntPage = (cntPage + 1) % pagelen
        elif signum == signal.SIGUSR2:
            # Key CONFIRM
            print 'K2 pressed'
        SHController.cntPage = cntPage

    @staticmethod
    def init():
        # this method should be called after registration is complete
        # register signal handlers
        img = Image.open('friendllyelec.png').convert('1')

        btn_handler = SHController.btn_handler
        signal.signal(signal.SIGUSR1, btn_handler)
        signal.signal(signal.SIGUSR2, btn_handler)
        signal.signal(signal.SIGALRM, btn_handler)
        while True:
            try:
                SHController.update()
            except KeyboardInterrupt:
                break
            except IOError:
                print "IOError"

    @staticmethod
    def register(pageView):
        # registers interactive page views
        if (not issubclass(type(pageView), SHPageView)):
            print "must register SHPageView object as page view, received " \
                + str(type(pageView))
            return
        udid = pageView.udid
        SHController.pages[udid] = pageView

