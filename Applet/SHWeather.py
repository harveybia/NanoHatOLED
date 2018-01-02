from SHFramework import *
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import time

class SHWeatherPageView(SHPageView):
    def __init__(self, name="WeatherView"):
        super(SHWeatherPageView, self).__init__(name)

    def getImage(self):
        img = Image.new('1', (SH_WIDTH, SH_HEIGHT))
        draw = ImageDraw.Draw(img)
        draw.text((2,2), 'Page '+str(self.udid), font=font14, fill=255)
        return img

class SHClockPageView(SHPageView):
    def __init__(self, name="ClockView"):
        super(SHClockPageView, self).__init__(name)

    def getImage(self):
        img = Image.new('1', (SH_WIDTH, SH_HEIGHT))
        draw = ImageDraw.Draw(img)
        text = time.ctime()[-13:]
        text2 = time.ctime()[0:10]
        draw.text((1,1), text, font=font14, fill=255)
        draw.text((1,15), text2, font=font14, fill=255)
        return img

# Main entry
view1 = SHWeatherPageView("WView1")
view2 = SHClockPageView("WView2")
SHController.register(view1)
SHController.register(view2)

SHController.init()
